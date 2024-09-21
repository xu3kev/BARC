#!/usr/bin/env python
# coding=utf-8

import os, os.path as osp
import random
import multiprocessing as mp

def main(seed=0):
    random.seed(seed)
    curdir = osp.dirname(osp.abspath(__file__))
    datadir = osp.join(curdir, 'cached_data')
    paths = list(os.walk(datadir))
    random.shuffle(paths)
    for root, dirs, files in paths:
        for f in files:
            if not os.path.exists(osp.join(root, f)):
                continue
            if f.endswith('.lock'):
                os.remove(osp.join(root, f))
                print('Removed:', osp.join(root, f))
            if f == 'cache.dill':
                os.remove(osp.join(root, f))
                print('Removed:', osp.join(root, f))

if __name__ == '__main__':
    with mp.Pool(8) as p:
        p.map(main, list(range(8)))
