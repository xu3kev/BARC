import os
from openai import OpenAI
from enum import Enum
import hashlib
import diskcache as dc
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import tiktoken
import json


class Provider(Enum):
    OPENAI = 'openai'
    GROQ = 'groq'
    DEEPSEEK = 'deepseek'
    VLLM = 'vllm'
    OPENROUTER = 'openrouter'

class OpenAIModels(Enum):
    GPT_4 = 'gpt-4'
    GPT_4_TURBO = 'gpt-4-turbo'
    GPT_4O = 'gpt-4o'
    GPT_35_TURBO = 'gpt-3.5-turbo'
    GPT_4O_MINI = 'gpt-4o-mini'
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

class GroqModels(Enum):
    LLAMA3_70B_8192 = 'llama3-70b-8192'
    MIXTRAL_8X7B_32768 = 'mixtral-8x7b-32768'

class DEEPSEEKModels(Enum):
    DEEPSEEKCODER = 'deepseek-coder'

class VLLMModels(Enum):
    LLAMA3_70B = 'meta-llama/Meta-Llama-3-70B-Instruct'

class OpenRouterModels(Enum):
    SONNET35 = "anthropic/claude-3.5-sonnet:beta"
    LLAMA3_70B = "meta-llama/llama-3-70b-instruct"
    DEEPSEEKCODER = "deepseek/deepseek-coder"

class LLMClient:
    AVAILABLE_MODELS = {
        Provider.OPENAI: OpenAIModels,
        Provider.GROQ: GroqModels,
        Provider.DEEPSEEK: DEEPSEEKModels,
        Provider.VLLM: VLLMModels,
        Provider.OPENROUTER: OpenRouterModels
    }

    model_cost = {
        "gpt-4": (30, 60),
        "gpt-4-turbo": (10, 30),
        "gpt-4-turbo-preview": (10, 30),
        "gpt-4-turbo-2024-04-09": (10, 30),
        "gpt-4o": (5, 15),
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o-2024-05-13": (5, 15),
        "gpt-3.5-turbo-0123": (0.50, 1.50),
        "gpt-3.5-turbo": (0.50, 1.50),
        "text-embedding-ada-002": (0.10, 0.10),
        "deepseek/deepseek-coder": (0.14, 0.28),
    }

    def __init__(self, system_content=None, provider=Provider.OPENAI, cache_dir='cache', key=None):
        self.provider = provider
        self.api_key = key or self._get_api_key()
        assert self.api_key is not None, f"API key not found for provider {self.provider}"
        self.system_content = system_content if system_content is not None else "You will be provided a few code examples on color grid input generator and transformation. You will be creative and come up with similar and interesting problems."
        self.client = self._initialize_client()
        self.cache = dc.Cache(cache_dir)
        self.usage_cache = dc.Cache(cache_dir + "_usage")
        self.total_input_tokens = {}
        self.total_output_tokens = {}

    def _get_api_key(self):
        if self.provider == Provider.GROQ:
            return os.getenv("GROQ_API_KEY")
        elif self.provider == Provider.DEEPSEEK:
            return os.getenv("DEEPSEEK_API_KEY")
        elif self.provider == Provider.VLLM:
            return "EMPTY"
        elif self.provider == Provider.OPENROUTER:
            return os.getenv("OPENROUTER_API_KEY")

        return os.getenv("OPENAI_API_KEY")

    def _initialize_client(self):
        if self.provider == Provider.GROQ:
            return OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
        elif self.provider == Provider.DEEPSEEK:
            return OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        elif self.provider == Provider.VLLM:
            return OpenAI(api_key="EMPTY", base_url="http://localhost:8100/v1")
        elif self.provider == Provider.OPENROUTER:
            return OpenAI(api_key=self.api_key, base_url="https://openrouter.ai/api/v1")
        return OpenAI(api_key=self.api_key)

    def _hash_prompt(self, prompt, model, temperature, max_tokens, top_p):
        # Create a unique hash for the given parameters
        hash_input = f"{prompt}-{model}-{temperature}-{max_tokens}-{self.system_content}-{top_p}".encode()
        return hashlib.md5(hash_input).hexdigest()
    
    def _hash_embedding(self, input, model):
        # Create a unique hash for the given parameters
        hash_input = f"{input}-{model}-{self.system_content}".encode()
        return hashlib.md5(hash_input).hexdigest()
    
    def update_usage(self, engine: str, usage: dict[str, int]):
        self.total_input_tokens[engine] = self.total_input_tokens.get(engine, 0) + usage.prompt_tokens
        self.total_output_tokens[engine] = self.total_output_tokens.get(engine, 0) + usage.total_tokens - usage.prompt_tokens
        self.add_usage_to_cache(engine, usage)

    def show_global_token_usage(self):
        for engine in self.model_cost.keys():
            usage = self.get_usage_from_cache(engine)
            i = usage["input_tokens"]
            o = usage["output_tokens"]
            # dollars per million tokens
            i_cost, o_cost = self.model_cost.get(engine, (0.0, 0.0))
            total_cost = i_cost*i/1e6 + o_cost*o/1e6

            print(f"{engine}: {i} input tokens (${i_cost:.02f}/1m tokens), {o} output tokens (${o_cost:.02f}/1m tokens)")
            print(" "*len(engine), f" total cost: ${total_cost:.02f}")

    def show_token_usage(self):
        for engine in self.total_input_tokens:
            i = self.total_input_tokens[engine]
            o = self.total_output_tokens[engine]
            # dollars per million tokens
            i_cost, o_cost = self.model_cost.get(engine, (0.0, 0.0))
            total_cost = i_cost*i/1e6 + o_cost*o/1e6

            print(f"{engine}: {i} input tokens (${i_cost:.02f}/1m tokens), {o} output tokens (${o_cost:.02f}/1m tokens)")
            print(" "*len(engine), f" total cost: ${total_cost:.02f}")

    def total_cost(self):
        total_cost = 0
        for engine in self.total_input_tokens:
            i = self.total_input_tokens[engine]
            o = self.total_output_tokens[engine]
            i_cost, o_cost = self.model_cost.get(engine, (0.0, 0.0))
            total_cost += i_cost*i/1000 + o_cost*o/1000
        return total_cost

    def n_tokens_in_prompt(self, prompt, engine):
        encoding = tiktoken.encoding_for_model(engine)
        if isinstance(prompt, str): prompt = [prompt]
        return sum( len(encoding.encode(p)) for p in prompt )

    def get_token_usage(self, engine):
        i = self.total_input_tokens.get(engine, 0)
        o = self.total_output_tokens.get(engine, 0)
        return i, o
    
    def add_usage_to_cache(self, engine, usage):
        cur = self.usage_cache.get(engine, {"input_tokens": 0, "output_tokens": 0})
        self.usage_cache[engine] = {"input_tokens": cur["input_tokens"] + usage.prompt_tokens, "output_tokens": cur["output_tokens"] + usage.total_tokens - usage.prompt_tokens}

    def get_usage_from_cache(self, model):
        return self.usage_cache.get(model, {"input_tokens": 0, "output_tokens": 0})

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

    def generate_request_json(self, prompt, model, temperature, max_tokens, top_p, num_samples):
        request = {
            "model":model.value,
            "messages":[
                {
                    "role": "system",
                    "content": self.system_content
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature":temperature,
            "max_tokens":max_tokens,
            "top_p":top_p,
            "n":num_samples
        }
        return request

    def batch_request(self, job_description, prompts, model, temperature, max_tokens, num_samples, top_p=1, blocking=False):
        """
        Uses the batch API to upload all the requests in a file and get the results
        if blocking, returns the final list of list of results (or None) when a result is missing
        if not blocking, returns a function that when called gives a tuple of (status, maybe_final_result)
        By default it does not block.
        """
        requests = [self.generate_request_json(p, model, temperature, max_tokens, top_p, num_samples) for p in prompts]
        # Create a file based on the job description called job_description_input.jsonl, and put each request in a line
        input_data = []
        for n, request in enumerate(requests):
            _request = {"custom_id": f"request-{n}", "method": "POST", "url": "/v1/chat/completions", "body": request}
            input_data.append(json.dumps(_request))
        input_data = "\n".join(input_data) + "\n"

        import io
        
        # Upload the file to the batch API
        batch_input_file = self.client.files.create(
            file=io.BytesIO(bytes(input_data, 'utf-8')), 
            purpose="batch"
        )

        batch_input_file_id = batch_input_file.id

        batch_job = self.client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
            "description": job_description
            }
        )

        def callback():
            nonlocal batch_job
            retrieval = self.client.batches.retrieve(batch_job.id)
            if "completed" in str(retrieval.status):
                data = self.client.files.content(retrieval.output_file_id).content
                # process the data as though it were jsonl: first convert from bytes to string
                data = data.decode("utf-8")
                # then iterate through the lines
                data = data.strip().split("\n")
                data = [json.loads(d) for d in data]
                response_dictionary = {}
                for entry in data:
                    index = int(entry["custom_id"].replace("request-", ""))
                    response_dictionary[index] = entry["response"].get("body", {}).get("choices", None)
                    if response_dictionary[index] is not None:
                        response_dictionary[index] = [c["message"]["content"] for c in response_dictionary[index]]
                
                data = [response_dictionary.get(i, None) for i in range(len(requests))]

            else:
                data = None
            return retrieval.status, data
        
        if not blocking: return callback

        start_time = time.time()
        while True:
            status, data = callback()
            if "completed" in str(status):
                pretty_printed_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
                print(f" [+] Batch job {job_description} completed in {pretty_printed_time}")
                return data
            print(f" [~] Status: {status}")
            time.sleep(5)


    def send_embedding_request(self, input, model):
        response = self.client.embeddings.create(
            model=model.value,
            input=input,
            encoding_format="float"
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
    
    def get_embedding_from_cache(self, input, model):
        # Create a unique hash for the prompt and parameters (excluding num_samples)
        cache_key = self._hash_embedding(input, model.value)
        return self.cache.get(cache_key, None)

    def add_samples_to_cache(self, prompt, model, temperature, max_tokens, top_p, samples):
        cache_key = self._hash_prompt(prompt, model.value, temperature, max_tokens, top_p)
        cached_samples = self.cache.get(cache_key, [])
        cached_samples.extend(samples)
        self.cache[cache_key] = cached_samples
    
    def add_embedding_to_cache(self, input, model, embedding):
        cache_key = self._hash_embedding(input, model.value)
        self.cache[cache_key] = embedding

    def generate(self, prompt, num_samples, model=None, temperature=0.7, max_tokens=800, top_p=1, ignore_cache_samples=False):
        model = self.check_model_name(model)
        if not ignore_cache_samples:
            cached_samples = self.get_samples_from_cache(prompt, model, temperature, max_tokens, top_p)
        else:
            cached_samples = []
        # If the number of cached samples is less than requested, generate more samples
        if len(cached_samples) < num_samples:
            remaining_samples = num_samples - len(cached_samples)
            actually_got_samples = False
            backoff_timer = 1
            while not actually_got_samples:
                try:
                    response = self.send_request(prompt, model, temperature, max_tokens, top_p, remaining_samples)
                    new_samples = [c.message.content for c in response.choices]
                    self.add_samples_to_cache(prompt, model, temperature, max_tokens, top_p, new_samples)
                    self.update_usage(model.value, response.usage)
                    actually_got_samples = True
                except Exception as e:
                    if "Rate limit reached for model" in str(e):
                        if backoff_timer > 120:
                            print("Request too big, skipping")
                            break
                        print("Rate limit reached, backoff for", backoff_timer, "seconds")
                        time.sleep(backoff_timer)
                        backoff_timer *= 2
                    elif "Bad Request" in str(e):
                        print("Bad Request, skipping")
                        print(e)
                        break
                    else:
                        print("Error, going to try again in 1 second", e)
                        time.sleep(1)

        # WARN neccessary to get the samples from cache again as it might have been updated
        cached_samples = self.get_samples_from_cache(prompt, model, temperature, max_tokens, top_p)

        # Return a subset of the cached samples if they are more than the requested number
        if len(cached_samples) > num_samples:
            return random.sample(cached_samples, num_samples)

        return cached_samples[:num_samples]
    
    def generate_embedding(self, input, model=None):
        """input can be a list, in which case we return a list of embeddings"""
        originally_list = isinstance(input, list)
        if not isinstance(input, list): input = [input]

        model = self.check_model_name(model)
        cached_embedding = [ self.get_embedding_from_cache(s, model) for s in input]

        need_to_compute = [ s for s, e in zip(input, cached_embedding) if e is None ]

        while len(need_to_compute) > 0:
            batch_size = 512
            next_batch = need_to_compute[:batch_size]
            need_to_compute = need_to_compute[batch_size:]

            actually_got_embeddings = False
            backoff_timer = 1
            while not actually_got_embeddings:
                try:
                    response = self.send_embedding_request(next_batch, model)
                    embeddings = [response.data[i].embedding for i in range(len(next_batch))]
                    for s, e in zip(next_batch, embeddings):
                        self.add_embedding_to_cache(s, model, e)
                    self.update_usage(model.value, response.usage)
                    actually_got_embeddings = True
                except Exception as e:
                    if "Rate limit reached for model" in str(e):
                        if backoff_timer > 120:
                            print("Request too big, skipping")
                            break
                        print("Rate limit reached, backoff for", backoff_timer, "seconds")
                        time.sleep(backoff_timer)
                        backoff_timer *= 2
                    elif "Bad Request" in str(e):
                        print("Bad Request, skipping")
                        break
                    else:
                        print("Error, going to try again in 1 second", e)
                        time.sleep(1)
                

        # WARN neccessary to get the samples from cache again as it might have been updated
        cached_embeddings = [self.get_embedding_from_cache(s, model) for s in input]

        return cached_embeddings[0] if not originally_list else cached_embeddings



    def generate_parallel(self, prompts, num_samples, model=None, temperature=0.7, max_tokens=800, top_p=1, num_workers=8):
        """use concurrent futures to generate samples in parallel"""
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self.generate, prompt, num_samples, model, temperature, max_tokens, top_p) for prompt in prompts]
            results = []
            for future in tqdm(as_completed(futures), total=len(futures), desc="Generating samples"):
                results.append(future.result())
            return results
        
    def generate_embedding_parallel(self, inputs, model=None, num_workers=8):
        """use concurrent futures to generate samples in parallel"""
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_index = {
                executor.submit(self.generate_embedding, input, model): i
                for i, input in enumerate(inputs)
            }
            results = [None] * len(inputs) # Pre-allocate the results list
            for future in tqdm(as_completed(future_to_index), total=len(future_to_index), desc="Generating embeddings"):
                index = future_to_index[future]
                results[index] = future.result()
            return results