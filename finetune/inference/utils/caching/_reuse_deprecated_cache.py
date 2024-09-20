#!/usr/bin/env python
# coding=utf-8

import os, os.path as osp
import dill

def main():
    curdir = osp.dirname(osp.abspath(__file__))
    cachedir = osp.join(curdir, 'cached_data')
    for root, dirs, files in os.walk(cachedir):
        for file in files:
            if file == 'cache.dill':
                print(f'Processing {root}')
                filepath = osp.join(root, file)
                with open(filepath, 'rb') as f:
                    cache = dill.load(f)
                response_dir = osp.join(root, 'response')
                os.makedirs(response_dir, exist_ok=True)
                for index, res in enumerate(cache['response']):
                    with open(osp.join(response_dir, f'{index}.dill'), 'wb') as f:
                        dill.dump(res, f)

                index_dir = osp.join(root, 'index')
                os.makedirs(index_dir, exist_ok=True)
                assert isinstance(cache['index'], dict), (f'cache["index"] must be a dict, got {type(cache["index"])}', root)
                for seed, cur_index in cache['index'].items():
                    cur_index_dir = osp.join(index_dir, str(seed))
                    os.makedirs(cur_index_dir, exist_ok=True)
                    for nth, idx in enumerate(cur_index):
                        with open(osp.join(cur_index_dir, f'{nth}_{idx}.txt'), 'w') as f:
                            f.write('')

if __name__ == '__main__':
    main()

