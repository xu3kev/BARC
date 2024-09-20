#!/usr/bin/env python
# coding=utf-8

import os
import shutil

import json, dill
import numpy as np
import hashlib

class _CacheSystem:
    def __init__(self, cache_path=None, seed=0, stochastic=False):
        if cache_path is None:
            curdir = os.path.dirname(os.path.abspath(__file__))
            cache_path = os.path.join(curdir, 'cached_data', self.__class__.__name__)
        self.cache_path = cache_path
        os.makedirs(self.cache_path, exist_ok=True)
        self.seed = seed
        self.stochastic = stochastic
        self.caches = {}
        self.nth_dict = {}
    def _action(self, *args, **kwargs):
        raise NotImplementedError
    def _cache_id(self, *args, **kwargs):
        raise NotImplementedError
    def __call__(self, *args, nth=None, **kwargs):
        #((name, id, value), ...)
        cache_id = self._cache_id(*args, **kwargs)
        assert isinstance(cache_id, tuple), f'cache_id must be a tuple, got {type(cache_id)}'
        assert all([len(cid)==3 for cid in cache_id]), f'cache_id must be a tuple of tuples of length 2, got {cache_id}'
        assert all([isinstance(cid[0], str) for cid in cache_id]), f'cache_id must be a tuple of tuples with first element being a string, got {cache_id}'
        assert all([isinstance(cid[1], str) for cid in cache_id]), f'cache_id must be a tuple of tuples with second element being a string, got {cache_id}'
        unique_cache_id = '_'.join([cid[1] for cid in cache_id])
        cache_path = self._get_cache_path(cache_id)

        # Get nth
        if self.stochastic:
            if nth is None:
                if unique_cache_id not in self.nth_dict:
                    self.nth_dict[unique_cache_id] = {}
                if self.seed not in self.nth_dict[unique_cache_id]:
                    self.nth_dict[unique_cache_id][self.seed] = 0
                self.nth_dict[unique_cache_id][self.seed] += 1
                nth = self.nth_dict[unique_cache_id][self.seed]
            else:
                assert len(self.nth_dict) == 0, 'nth_dict must be empty for deterministic nth'
        else:
            nth = 1

        # Handle cache
        if unique_cache_id in self.caches and self.seed in self.caches[unique_cache_id]['index'] and nth < len(self.caches[unique_cache_id]['index'][self.seed]):
            cache = self.caches[unique_cache_id]
        elif os.path.exists(cache_path):
            cache = self._load_cache(cache_path)
        else:
            cache = {'response': [], 'index': {}}

        # Found index
        if self.seed in cache['index']:
            index = cache['index'][self.seed]
            if len(index) < len(cache['response']):
                np_rng = np.random.default_rng(self.seed)
                index = index + list(np_rng.permutation(list(range(len(index), len(cache['response'])))))
        elif len(cache['response']):
            np_rng = np.random.default_rng(self.seed)
            index = list(np_rng.permutation(list(range(len(cache['response'])))))
        else:
            index = []

        # Get response
        if nth > len(index):
            assert nth == len(index)+1, f'Expected nth to be {len(index)+1}, got {nth}'
            response = self._action(*args, **kwargs)
            cache['response'].append(response)
            index.append(len(cache['response'])-1)
            cache['index'][self.seed] = index
            updated_cache = True
        else:
            updated_cache = False
        response = cache['response'][index[nth-1]]

        # Save cache
        if updated_cache:
            self.caches[unique_cache_id] = cache
            self._save_cache(cache, cache_path)

        return response
    def _get_cache_path(self, cache_id):
        path = self.cache_path
        seen_values = []
        for name, cid, value in cache_id:
            path = os.path.join(path, f'{name}_{cid}')
            os.makedirs(path, exist_ok=True)
            seen_values.append(value)
            if (
                not os.path.exists(os.path.join(path, 'value.json')) and
                not os.path.exists(os.path.join(path, 'value.dill')) and
                not os.path.exists(os.path.join(path, 'seen_values.json')) and
                not os.path.exists(os.path.join(path, 'seen_values.dill'))
            ):
                if len(str(value)) < 1e5:
                    try:
                        with open(os.path.join(path, 'value.json'), 'w') as f:
                            json.dump(value, f)
                    except:
                        with open(os.path.join(path, 'value.dill'), 'wb') as f:
                            dill.dump(value, f)
                else:
                    with open(os.path.join(path, 'value.json'), 'w') as f:
                        json.dump('value too long', f)
                if len(str(seen_values)) < 1e5:
                    try:
                        with open(os.path.join(path, 'seen_values.json'), 'w') as f:
                            json.dump(seen_values, f)
                    except:
                        with open(os.path.join(path, 'seen_values.dill'), 'wb') as f:
                            dill.dump(seen_values, f)
                else:
                    with open(os.path.join(path, 'seen_values.json'), 'w') as f:
                        json.dump('seen_values too long', f)
        path = os.path.join(path, 'cache.dill')
        return path
    def _load_cache(self, cache_path):
        with open(cache_path, 'rb') as f:
            try:
                cache = dill.load(f)
            except Exception as e:
                print(f'Failed to load cache from {cache_path} due to {e}')
                raise e
        return cache
    def _save_cache(self, cache, cache_path):
        # Copy cache to avoid modifying the original cache
        if os.path.exists(cache_path):
            shutil.copyfile(cache_path, cache_path+'.bak')
        while True:
            try:
                with open(cache_path, 'wb') as f:
                    dill.dump(cache, f)
                with open(cache_path, 'rb') as f:
                    dill.load(f)
                break
            except Exception as e:
                print(f'Failed to save cache to {cache_path} due to {e}')
    @classmethod
    def _value2id(cls, value):
        canonical_value = cls._canonical_value(value)
        vid = hashlib.md5(str(canonical_value).encode('utf-8')).hexdigest()
        return vid
    @classmethod
    def _canonical_value(cls, value):
        if isinstance(value, dict):
            value = {k: cls._canonical_value(v) for k, v in value.items()}
            return tuple(sorted(value.items(), key=str))
        elif isinstance(value, list):
            value = [cls._canonical_value(v) for v in value]
            return tuple(value)
        elif isinstance(value, tuple):
            return tuple([cls._canonical_value(v) for v in value])
        elif isinstance(value, set):
            return tuple(sorted([cls._canonical_value(v) for v in value], key=str))
        elif isinstance(value, np.ndarray):
            return cls._canonical_value(value.tolist())
        else:
            return value
    def set_seed(self, seed):
        self.seed = seed



