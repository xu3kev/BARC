import os
from openai import OpenAI
from enum import Enum
import hashlib
import diskcache as dc
import random


class Provider(Enum):
    OPENAI = 'openai'
    GROQ = 'groq'

class OpenAIModels(Enum):
    GPT_4_TURBO = 'gpt-4-turbo'
    GPT_4O = 'gpt-4o'

class GroqModels(Enum):
    LLAMA3_70B_8192 = 'llama3-70b-8192'
    MIXTRAL_8X7B_32768 = 'mixtral-8x7b-32768'

class LLMClient:
    AVAILABLE_MODELS = {
        Provider.OPENAI: OpenAIModels,
        Provider.GROQ: GroqModels
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
        return os.getenv("OPENAI_API_KEY")

    def _initialize_client(self):
        if self.provider == Provider.GROQ:
            return OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
        return OpenAI(api_key=self.api_key)

    def _hash_prompt(self, prompt, model, temperature, max_tokens, top_p):
        # Create a unique hash for the given parameters
        hash_input = f"{prompt}-{model}-{temperature}-{max_tokens}-{self.system_content}-{top_p}".encode()
        return hashlib.md5(hash_input).hexdigest()

    def generate(self, prompt, num_samples, model=None, temperature=0.7, max_tokens=800, top_p=1):
        model_enum = self.AVAILABLE_MODELS[self.provider]
        if model is None:
            model = list(model_enum)[0]
        elif not isinstance(model, model_enum):
            raise ValueError(f"Model {model} is not available for provider {self.provider}")

        # Create a unique hash for the prompt and parameters (excluding num_samples)
        cache_key = self._hash_prompt(prompt, model.value, temperature, max_tokens, top_p)

        # Check if the result is already in the cache
        cached_samples = self.cache.get(cache_key, [])

        # If the number of cached samples is less than requested, generate more samples
        if len(cached_samples) < num_samples:
            remaining_samples = num_samples - len(cached_samples)
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
                n=remaining_samples
            )
            new_samples = [c.message.content for c in response.choices]
            cached_samples.extend(new_samples)
            self.cache[cache_key] = cached_samples

        # Return a subset of the cached samples if they are more than the requested number
        if len(cached_samples) > num_samples:
            return random.sample(cached_samples, num_samples)
        return cached_samples[:num_samples]
