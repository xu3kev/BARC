#!/usr/bin/env python
# coding=utf-8

import os
import json
import copy
import tiktoken
import pickle

from .eval_utils import eval_code

def extract_code_blocks(message):
    code_blocks = []
    in_code_block = False
    for line in message.split("\n"):
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_blocks[-1] = "\n".join(code_blocks[-1])
            else:
                in_code_block = True
                code_blocks.append([])
        elif in_code_block:
            code_blocks[-1].append(line)
    if in_code_block:
        code_blocks[-1] = "\n".join(code_blocks[-1])
    return code_blocks

def _eq(a, b):
    try:
        return a == b
    except Exception as e:
        print(f'Warning: eq error, {e}, {a}, {b}, {type(a)}, {type(b)}')
        if len(a) != len(b):
            return False
        if type(a) != type(b):
            return False
        return all([a_ == b_ for a_, b_ in zip(a, b)])
def remove_duplicate_codes(codes):
    exec_globals = {}
    exec_globals = eval_code(codes, exec_globals=exec_globals, return_exec_globals=True)
    if not isinstance(exec_globals, dict):
        return codes
    codes = '\n'.join([l for l in codes.split('\n') if l.strip() or l.startswith('#')])

    lines = codes.split('\n')
    code_blocks = []
    prv_index = 0
    prv_exec_globals = dict()
    for index in range(len(lines)):
        if index < len(lines)-1 and len(lines[index+1].lstrip()) != len(lines[index+1]):
            continue
        if index < len(lines)-1 and lines[index].startswith('#'):
            continue
        if index < len(lines)-1 and (lines[index+1].startswith('else:') or lines[index+1].startswith('elif ')):
            continue
        try:
            _local_exec_globals = copy.deepcopy(prv_exec_globals)
        except Exception as e:
            # print(e)
            # print(prv_exec_globals)
            # print(lines[:index])
            _local_exec_globals = None
        if _local_exec_globals is not None:
            exec_globals = eval_code('\n'.join(lines[:index+1]), exec_globals=copy.deepcopy(prv_exec_globals), return_exec_globals=True)
        else:
            exec_globals = eval_code('\n'.join(lines[:index+1]), exec_globals=dict(), return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            assert index != len(lines)-1, (f'index == len(lines)-1, {index} == {len(lines)-1}', codes)
            continue
        exec_globals = {k: v for k, v in prv_exec_globals.items()}
        exec_globals = eval_code('\n'.join(lines[prv_index:index+1]), exec_globals=exec_globals, return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            # assert index != len(lines)-1, (f'index == len(lines)-1, {index} == {len(lines)-1}', codes, '\n'.join(lines[prv_index:index+1]))
            continue
        # exec('\n'.join(lines[prv_index:index+1]), exec_globals)
        update_vars = [
            k
            for k in exec_globals
            if (
                not k.startswith('__') and
                k != 'evaluate' and
                isinstance(k, str) and
                # callable(exec_globals[k]) and
                (k not in [kk for kk in prv_exec_globals if isinstance(kk, str)] or not _eq(exec_globals[k], prv_exec_globals[k]))
            )
        ]
        # assert len(update_vars) <= 1, (f'len(update_vars) != 1, {len(update_vars)} != 1', update_vars, codes)
        if len(update_vars) == 0:
            prv_index = index + 1
            continue
        code_blocks.append((
            update_vars,
            '\n'.join(lines[prv_index:index+1]),
        ))
        prv_index = index + 1
        prv_exec_globals = exec_globals
    # assert prv_index == len(lines), (f'prv_index != len(lines), {prv_index} != {len(lines)}', codes)

    deduplicated_code_blocks = []
    seen_vars = set()
    for var_list, code in code_blocks[::-1]:
        # assert len(var_list) == 1, f'len(var_list) != 1, {len(var_list)} != 1'
        if any([v not in seen_vars for v in var_list]):
            deduplicated_code_blocks.append(code)
            seen_vars.update(var_list)
    deduplicated_code_blocks = deduplicated_code_blocks[::-1]

    return '\n'.join(deduplicated_code_blocks)
def remove_unused_codes(codes, entry_point):
    codes = remove_duplicate_codes(codes)
    exec_globals = {}
    exec_globals = eval_code(codes, exec_globals=exec_globals, return_exec_globals=True)
    if not isinstance(exec_globals, dict):
        return codes
    codes = '\n'.join([l for l in codes.split('\n') if l.strip() or l.startswith('#')])

    lines = codes.split('\n')
    code_blocks = {}
    prv_index = 0
    prv_exec_globals = dict()
    for index in range(len(lines)):
        if index < len(lines)-1 and len(lines[index+1].lstrip()) != len(lines[index+1]):
            continue
        if index < len(lines)-1 and lines[index].startswith('#'):
            continue
        if index < len(lines)-1 and (lines[index+1].startswith('else:') or lines[index+1].startswith('elif ')):
            continue
        try:
            _local_exec_globals = copy.deepcopy(prv_exec_globals)
        except Exception as e:
            _local_exec_globals = None
        if _local_exec_globals is not None:
            exec_globals = eval_code('\n'.join(lines[:index+1]), exec_globals=copy.deepcopy(prv_exec_globals), return_exec_globals=True)
        else:
            exec_globals = eval_code('\n'.join(lines[:index+1]), exec_globals=dict(), return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            assert index != len(lines)-1, (f'index == len(lines)-1, {index} == {len(lines)-1}', codes)
            continue
        exec_globals = {k: v for k, v in prv_exec_globals.items()}
        exec_globals = eval_code('\n'.join(lines[prv_index:index+1]), exec_globals=exec_globals, return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            continue
        update_vars = [
            k
            for k in exec_globals
            if (
                not k.startswith('__') and
                k != 'evaluate' and
                isinstance(k, str) and
                # callable(exec_globals[k]) and
                (k not in [kk for kk in prv_exec_globals if isinstance(kk, str)] or not _eq(exec_globals[k], prv_exec_globals[k]))
            )
        ]
        if len(update_vars) == 0:
            prv_index = index + 1
            continue
        assert tuple(sorted(set(update_vars))) not in code_blocks, (f'set(update_vars) in code_blocks, {set(update_vars)} in {code_blocks}', codes)
        code_blocks[tuple(sorted(set(update_vars)))] = '\n'.join(lines[prv_index:index+1])
        prv_index = index + 1
        prv_exec_globals = exec_globals

    assert entry_point in prv_exec_globals, (f'entry_point not in prv_exec_globals, {entry_point} not in {prv_exec_globals}', codes)
    useful_vars = set([entry_point])
    while True:
        useful_codes = '\n'.join([code for var_list, code in code_blocks.items() if set(var_list).intersection(useful_vars)])
        cur_useful_vars = useful_vars.copy()
        for var_list, code in code_blocks.items():
            if set(var_list).intersection(cur_useful_vars) or any([v in useful_codes for v in var_list]):
                cur_useful_vars.update(var_list)
        if useful_vars == cur_useful_vars:
            break
        useful_vars = cur_useful_vars
    useful_codes = '\n'.join([code for var_list, code in code_blocks.items() if code.strip().startswith('class ') or set(var_list).intersection(useful_vars)])

    return useful_codes

def abbr_repr(obj, max_len=100):
    if isinstance(obj, dict):
        return {
            k: abbr_repr(v, max_len=max_len)
            for k, v in obj.items()
            if len(str(abbr_repr(v, max_len=max_len))) < max_len
        }
    elif isinstance(obj, list):
        return [
            abbr_repr(v, max_len=max_len)
            for v in obj
            if len(str(abbr_repr(v, max_len=max_len))) < max_len
        ]
    elif isinstance(obj, tuple):
        return tuple(
            abbr_repr(v, max_len=max_len)
            for v in obj
            if len(str(abbr_repr(v, max_len=max_len))) < max_len
        )
    elif isinstance(obj, set):
        return {
            abbr_repr(v, max_len=max_len)
            for v in obj
            if len(str(abbr_repr(v, max_len=max_len))) < max_len
        }
    elif isinstance(obj, str):
        return obj[:max_len]
    else:
        return obj

def count_tokens_for_openai(mess, model='gpt-4'):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(mess))

def remove_noncompilable_code_blocks(code_blocks, prefix=''):
    idx = 0
    code_blocks = copy.deepcopy(code_blocks)
    while idx < len(code_blocks):
        codes = '\n'.join(code_blocks[:idx+1])
        exec_globals = eval_code(prefix+'\n'+codes, exec_globals=dict(), return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            exec_globals = eval_code(codes, exec_globals=dict(), return_exec_globals=True)
        if not isinstance(exec_globals, dict):
            code_blocks = code_blocks[:idx] + code_blocks[idx+1:]
        else:
            idx += 1
    return code_blocks

def get_avoid_words(key_words=None,):
    raise NotImplementedError
    curdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(curdir, 'avoid_words.json'), 'r') as f:
        avoid_words = json.load(f)
    avoid_words = {
        k:-100
        for k, v in avoid_words.items()
        if key_words is None or any([w.lower() in v.lower() for w in key_words])
    }
    return avoid_words

def pickable(data):
    try:
        pickle.dumps(data)
        return data
    except:
        pass
    if isinstance(data, dict):
        return {
            k: pickable(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [
            pickable(v)
            for v in data
        ]
    elif isinstance(data, tuple):
        return tuple(
            pickable(v)
            for v in data
        )
    elif isinstance(data, set):
        return {
            pickable(v)
            for v in data
        }
    elif isinstance(data, str):
        return data
    elif isinstance(data, int):
        return data
    elif isinstance(data, float):
        return data
    elif isinstance(data, bool):
        return data
    elif data is None:
        return data
    else:
        return str(data)

def itemnum(data):
    if isinstance(data, dict):
        return sum([itemnum(v) for v in data.values()])
    elif isinstance(data, list):
        return sum([itemnum(v) for v in data])
    elif isinstance(data, tuple):
        return sum([itemnum(v) for v in data])
    elif isinstance(data, set):
        return sum([itemnum(v) for v in data])
    elif isinstance(data, str):
        return len(data)
    else:
        return 1
