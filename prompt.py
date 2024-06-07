import os
import re
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

    def __init__(self, system_content=None, provider=Provider.OPENAI, cache_dir='cache'):
        self.provider = provider
        self.api_key = self._get_api_key()
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

def parse_code(paragraph):
    """
    This function extracts all Markdown code blocks from a given paragraph.
    Args:
        paragraph (str): The input paragraph containing the Markdown code blocks.
    Returns:
        list: A list of extracted code blocks.
    """
    # Regular expression to match Markdown code blocks
    code_block_pattern = re.compile(r"```python(.*?)```", re.DOTALL)

    # Find all code blocks in the paragraph
    matches = code_block_pattern.findall(paragraph)

    # Strip any leading/trailing whitespace from each code block
    code_blocks = [match.strip() for match in matches]

    return code_blocks

if __name__ == "__main__":
    # get all files in seeds directory
    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]

    # print all files
    for seed in seeds:
        print(seed)

    seed_content = []
    for seed in seeds:
        with open(f"seeds/{seed}") as f:
            content = f.read()
            assert "# ============= remove below this point for prompting =============" in content
            content = content.split("# ============= remove below this point for prompting =============")[0]
            seed_content.append(content)

    with open("seeds/common.py") as f:
        common_lib = f.read()
    prompt = "The following code examples describe a function that generates a color grid input and a function that transforms the input grid to output grid. Later, the input and output grids will be given to students as puzzle. The puzzle is to figure out the rule that transforms the input grid to output grid. The puzzles should be interesting and challenging for students to solve. You will be creative and come up with similar and interesting problems. You can use the provided code examples as a reference to create your own problems."

    prompt += "\n\n# Common Library:\n\n```python\n" + common_lib + "\n```\n"
    for i in range(len(seed_content)):
        prompt += "\n\n# Example:\n\n```python\n"+ seed_content[i] + "\n```\n"

    prompt += "\n\n# Your task is to create similar and interesting problems. You can use the provided code examples as a reference to create your own problems."

    client = LLMClient()
    samples = client.generate(prompt, 32)

    codes = []
    for sample in samples:
        codes.extend(parse_code(sample))
