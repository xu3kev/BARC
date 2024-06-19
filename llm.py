import os
from openai import OpenAI
from enum import Enum
import hashlib
import diskcache as dc
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


class Provider(Enum):
    OPENAI = 'openai'
    GROQ = 'groq'
    DEEPSEEK = 'deepseek'

class OpenAIModels(Enum):
    GPT_4_TURBO = 'gpt-4-turbo'
    GPT_4O = 'gpt-4o'
    GPT_35_TURBO = 'gpt-3.5-turbo'

class GroqModels(Enum):
    LLAMA3_70B_8192 = 'llama3-70b-8192'
    MIXTRAL_8X7B_32768 = 'mixtral-8x7b-32768'

class DEEPSEEKModels(Enum):
    DEEPSEEKCODER = 'deepseek-coder'

class LLMClient:
    AVAILABLE_MODELS = {
        Provider.OPENAI: OpenAIModels,
        Provider.GROQ: GroqModels,
        Provider.DEEPSEEK: DEEPSEEKModels
    }

    def __init__(self, system_content=None, provider=Provider.OPENAI, cache_dir='cache', key=None):
        self.provider = provider
        self.api_key = key or self._get_api_key()
        assert self.api_key is not None, f"API key not found for provider {self.provider}"
        self.system_content = system_content if system_content is not None else "You will be provided a few code examples on color grid input generator and transformation. You will be creative and come up with similar and interesting problems."
        self.client = self._initialize_client()
        self.cache = dc.Cache(cache_dir)

    def _get_api_key(self):
        if self.provider == Provider.GROQ:
            return os.getenv("GROQ_API_KEY")
        elif self.provider == Provider.DEEPSEEK:
            return os.getenv("DEEPSEEK_API_KEY")
        return os.getenv("OPENAI_API_KEY")

    def _initialize_client(self):
        if self.provider == Provider.GROQ:
            return OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
        elif self.provider == Provider.DEEPSEEK:
            return OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        return OpenAI(api_key=self.api_key)

    def _hash_prompt(self, prompt, model, temperature, max_tokens, top_p):
        # Create a unique hash for the given parameters
        hash_input = f"{prompt}-{model}-{temperature}-{max_tokens}-{self.system_content}-{top_p}".encode()
        return hashlib.md5(hash_input).hexdigest()

    def send_request(self, prompt, model, temperature, max_tokens, top_p, num_samples):
        response = self.client.chat.completions.create(
            model=model.value,
            messages=[
                {
                    "role": "system",
                    "content": self.system_content
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            n=num_samples
        )
        return response

    def check_model_name(self, model):
        model_enum = self.AVAILABLE_MODELS[self.provider]
        if model is None:
            model = list(model_enum)[0]
            print(f"Model name not provided, using default {model}")
        elif not isinstance(model, model_enum):
            raise ValueError(f"Model {model} is not available for provider {self.provider}")
        return model

    def get_samples_from_cache(self, prompt, model, temperature, max_tokens, top_p):
        # Create a unique hash for the prompt and parameters (excluding num_samples)
        cache_key = self._hash_prompt(prompt, model.value, temperature, max_tokens, top_p)
        return self.cache.get(cache_key, [])

    def add_samples_to_cache(self, prompt, model, temperature, max_tokens, top_p, samples):
        cache_key = self._hash_prompt(prompt, model.value, temperature, max_tokens, top_p)
        cached_samples = self.cache.get(cache_key, [])
        cached_samples.extend(samples)
        self.cache[cache_key] = cached_samples

    def generate(self, prompt, num_samples, model=None, temperature=0.7, max_tokens=800, top_p=1):
        model = self.check_model_name(model)
        cached_samples = self.get_samples_from_cache(prompt, model, temperature, max_tokens, top_p)

        # If the number of cached samples is less than requested, generate more samples
        if len(cached_samples) < num_samples:
            remaining_samples = num_samples - len(cached_samples)
            response = self.send_request(prompt, model, temperature, max_tokens, top_p, remaining_samples)
            new_samples = [c.message.content for c in response.choices]
            self.add_samples_to_cache(prompt, model, temperature, max_tokens, top_p, new_samples)

        # WARN neccessary to get the samples from cache again as it might have been updated
        cached_samples = self.get_samples_from_cache(prompt, model, temperature, max_tokens, top_p)

        # Return a subset of the cached samples if they are more than the requested number
        if len(cached_samples) > num_samples:
            return random.sample(cached_samples, num_samples)

        return cached_samples[:num_samples]

    def generate_parallel(self, prompts, num_samples, model=None, temperature=0.7, max_tokens=800, top_p=1, num_workers=8):
        """use concurrent futures to generate samples in parallel"""
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self.generate, prompt, num_samples, model, temperature, max_tokens, top_p) for prompt in prompts]
            results = []
            for future in tqdm(as_completed(futures), total=len(futures), desc="Generating samples"):
                results.append(future.result())
            return results