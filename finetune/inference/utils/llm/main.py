#!/usr/bin/env python
# coding=utf-8

import copy
import hashlib

# from openai import AzureOpenAI
from openai import OpenAI
import time
from ..caching import _CacheSystem

def add_llm_args(parser):
    # gpt35 gpt4t
    parser.add_argument('--llm-port', type=str, help="API server for vllm")
    parser.add_argument('--llm-name', type=str, help="Your model unique name")
    parser.add_argument('--llm-temperature', type=float, default=1.0, help="The temperature to use for LLM")
    parser.add_argument('--llm-seed', type=int, default=None, help="The seed to use for LLM")
    
def get_llm(args, base_url):
    if args.llm_seed is None:
        # assert 'seed' in dir(args), f"args: {args}"
        # assert args.seed is not None, f"args: {args}"
        args.llm_seed = args.seed if 'seed' in dir(args) and args.seed is not None else 0
    return LLM(base_url=base_url, default_args={
        'model': 'models/' + args.model_name,
        'temperature': args.llm_temperature,
    }, seed=args.llm_seed,)

class LLM:
    def __init__(self, base_url, seed=0, default_args={'model': 'gpt4', 'temperature': 1.0,},):
        self.llm = _LLM(base_url=base_url, seed=seed, default_args=copy.deepcopy(default_args))
        self.tracker = LLMUsageTracker()
    def __call__(self, prompt, model_args=None):
        completion = self.llm(prompt, model_args)
        self.tracker.update(completion)
        return completion
    def track(self, name=None):
        return self.tracker.track(name)
    @property
    def default_args(self):
        return self.llm.default_args
    def set_seed(self, seed):
        self.llm.set_seed(seed)

class _LLM(_CacheSystem):
    def __init__(self, base_url, seed=0, default_args={'model': 'gpt4', 'temperature': 1.0,}):
        super(_LLM, self).__init__(seed=seed, stochastic=True,)
        self.default_args = default_args
        # self.client = AzureOpenAI(
        #     azure_endpoint='https://reap2-hao-ext.openai.azure.com/',
        #     api_version='2024-02-15-preview',
        #     api_key='96f167c63d2248899e861b9429c1ff74',
        # )
        self.client = OpenAI(api_key="EMPTY", base_url=base_url)
        self.local_tracker = LLMUsageTracker()
    def _action(self, prompt, model_args=None):
        BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        input_tokens = tokenizer.apply_chat_template([
            {"role":"system", "content":prompt[0]["content"]},
            {"role":"user", "content":prompt[1]["content"]}
        ], tokenize=True, add_generation_prompt=True)
        if len(input_tokens) > 7000:
            print("Input tokens too long")
            return None
        model_args = self._merge_args(model_args)
        max_try = 3
        # TODO: handle Error and Retry
        for _ in range(max_try):
            try:
                out = self.client.chat.completions.create(messages=prompt, **model_args)
                break
            except Exception as e:
                error_message = str(e)
                if "This model's maximum context length is 128000 tokens." in error_message:
                    return None
                print(e)
                time.sleep(3)
        self.local_tracker.update(out)
        return out
    def _cache_id(self, prompt, model_args=None):
        assert isinstance(prompt, list), f"prompt: {prompt}"
        assert all(isinstance(p, dict) for p in prompt), f"prompt: {prompt}"
        model_args = self._merge_args(model_args)
        assert isinstance(model_args, dict), f"model_args: {model_args}"
        prompt_id = hashlib.md5(str(prompt).encode()).hexdigest()
        model_args_id = '-'.join([f"{k}_{str(v)}" for k, v in model_args.items()])
        return (
            ('prompt', prompt_id, prompt),
            ('model_args', model_args_id, model_args),
        )
    def _merge_args(self, model_args):
        args = copy.deepcopy(self.default_args)
        if model_args is not None:
            args.update(model_args)
        return args
    def track(self, name=None):
        return self.local_tracker.track(name)
    def __getstate__(self):
        return {
            'seed': self.seed,
            'default_args': self.default_args,
            'local_tracker': self.local_tracker,
        }
    def __setstate__(self, state):
        self.seed = state['seed']
        self.default_args = state['default_args']
        self.local_tracker = state['local_tracker']

class LLMUsageTracker:
    def __init__(self,):
        self.usage = {
            'requests': 0,
            'completion_tokens': 0,
            'prompt_tokens': 0,
            'total_tokens': 0,
        }
        self.minor_trackers = {}
    def update(self, completion):
        self.usage['requests'] += 1
        if completion is None:
            return
        self.usage['completion_tokens'] += completion.usage.completion_tokens
        self.usage['prompt_tokens'] += completion.usage.prompt_tokens
        self.usage['total_tokens'] += completion.usage.total_tokens
    def __str__(self):
        return str(self.usage)
    def __repr__(self):
        return str(self.usage)
    def track(self, name=None):
        if name is None:
            return MinorLLMUsageTracker(self, name)
        if name not in self.minor_trackers:
            self.minor_trackers[name] = MinorLLMUsageTracker(self, name)
        return self.minor_trackers[name]
class MinorLLMUsageTracker():
    def __init__(self, tracker, name):
        self.name = name
        self.tracker = tracker
        self.usage = {
            'requests': 0,
            'completion_tokens': 0,
            'prompt_tokens': 0,
            'total_tokens': 0,
        }
    def __enter__(self,):
        self.start = copy.deepcopy(self.tracker.usage)
        return self
    def __exit__(self, type, value, traceback):
        self.end = copy.deepcopy(self.tracker.usage)
        self.usage['requests'] += self.end['requests'] - self.start['requests']
        self.usage['completion_tokens'] += self.end['completion_tokens'] - self.start['completion_tokens']
        self.usage['prompt_tokens'] += self.end['prompt_tokens'] - self.start['prompt_tokens']
        self.usage['total_tokens'] += self.end['total_tokens'] - self.start['total_tokens']
    def __str__(self):
        return str(self.usage)
    def __repr__(self):
        return str(self.usage)