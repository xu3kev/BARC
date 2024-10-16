#!/usr/bin/env python
# coding=utf-8

import os
import shutil

import json, dill
import numpy as np
import hashlib
import time

class _CacheSystem:
    def __init__(self, cache_path=None, seed=0, stochastic=False):
        if cache_path is None:
            curdir = os.path.dirname(os.path.abspath(__file__))
            cache_path = os.path.join(curdir, 'cached_data', self.__class__.__name__)
        self.cache_path = cache_path
        os.makedirs(self.cache_path, exist_ok=True)
        self.seed = seed
        self.stochastic = stochastic
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
                    self.nth_dict[unique_cache_id][self.seed] = -1
                self.nth_dict[unique_cache_id][self.seed] += 1
                nth = self.nth_dict[unique_cache_id][self.seed]
            else:
                assert len(self.nth_dict) == 0, 'nth_dict must be empty for deterministic nth'
        else:
            nth = 0
        
        # Generate new response if needed
        response_path = os.path.join(cache_path, 'response')
        os.makedirs(response_path, exist_ok=True)
        response_num = len([fn for fn in os.listdir(response_path) if fn.endswith('.dill')])
        if response_num <= nth:
            assert response_num == nth, f'Expected response_num to be {nth}, got {response_num}'

            if os.path.exists(os.path.join(response_path, f'{nth}.lock')):
                sleep_time, slept_times = 1, 0
                while os.path.exists(os.path.join(response_path, f'{nth}.lock')):
                    print(f'Waiting for {response_path}/{nth}.lock to be released, slept for {slept_times} seconds')
                    time.sleep(sleep_time)
                    slept_times += sleep_time
                    sleep_time *= 2
                    if slept_times > 2:
                        print(f'Waited for {response_path}/{nth}.lock for too long')
                        break
                if os.path.exists(os.path.join(response_path, f'{nth}.dill')):
                    print(f'Found {response_path}/{nth}.dill, skipping generation')
                else:
                    print(f'Waited for {response_path}/{nth}.lock for too long, removing lock, and regenerating')
                    os.remove(os.path.join(response_path, f'{nth}.lock'))

            if not os.path.exists(os.path.join(response_path, f'{nth}.dill')):
                with open(os.path.join(response_path, f'{nth}.lock'), 'w') as f:
                    f.write('lock')
                print(f'Generating {response_path}/{nth}.dill')
                # todo for reuse databse
                response = self._action(*args, **kwargs)
                if not os.path.exists(os.path.join(response_path, f'{nth}.dill')):
                    assert os.path.exists(os.path.join(response_path, f'{nth}.lock')), f'Expected {response_path}/{nth}.lock to exist, got {os.listdir(response_path)}'
                    with open(os.path.join(response_path, f'{nth}.dill'), 'wb') as f:
                        dill.dump(response, f)
                    os.remove(os.path.join(response_path, f'{nth}.lock'))
                else:
                    print(f'Found {response_path}/{nth}.dill, skipping generation')

            assert os.path.exists(os.path.join(response_path, f'{nth}.dill')), (f'Expected response to be saved, got {os.listdir(response_path)}', response_path, nth)
            assert not os.path.exists(os.path.join(response_path, f'{nth}.lock')), f'Expected {response_path}/{nth}.lock to be removed, got {os.listdir(response_path)}'
            response_num += 1

        # Found index
        index_path = os.path.join(cache_path, 'index')
        os.makedirs(index_path, exist_ok=True)
        index_path = os.path.join(index_path, f'{self.seed}')
        os.makedirs(index_path, exist_ok=True)
        index_length = len(os.listdir(index_path))
        index = {_nth: _index for _nth, _index in [
            (int(fn.split('.')[0].split('_')[0]), int(fn.split('.')[0].split('_')[1]))
            for fn in os.listdir(index_path)
        ]}
        assert set(index.keys()) == set(range(index_length)), f'Expected index to be {set(range(index_length))}, got {set(index.keys())}'
        if index_length <= nth:
            assert index_length == nth, f'Expected index_length to be {nth}, got {index_length}'
            np_rng = np.random.default_rng(self.seed)
            unseen_index = list(sorted(list(set(range(response_num)) - set(index.values()))))
            chosed_index = np_rng.choice(unseen_index)
            with open(os.path.join(index_path, f'{nth}_{chosed_index}.txt'), 'w') as f:
                f.write('')
            index_length += 1
            index[nth] = chosed_index
        index = index[nth]

        # Load response
        assert os.path.exists(os.path.join(response_path, f'{index}.dill')), (f'Expected response to be saved, got {os.listdir(response_path)}', response_path, index)
        # print('Loading cache', os.path.join(response_path, f'{index}.dill'))
        with open(os.path.join(response_path, f'{index}.dill'), 'rb') as f:
            response = dill.load(f)

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
        return path
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



