import os
import re
from openai import OpenAI
from enum import Enum
import hashlib
import diskcache as dc
import random
from func_timeout import func_timeout, FunctionTimedOut
from utils import extract_functions, extract_function_calls, extract_class_definitions
import sys
# add seeds/ to the python path
sys.path.append("seeds/")


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

def make_prompt(seeds, rng_seed, remix=0):
    """
    remix: how many example seeds the prompt tells the LLM to remix (0 means no remixing, just shows all the seeds)
    """
    # make a random generator
    rng = random.Random(rng_seed)

    # Sort the seeds so that the order is consistent
    seeds = list(sorted(seeds))

    seed_content = []
    for seed in seeds:
        with open(f"seeds/{seed}") as f:
            content = f.read()
            assert "# ============= remove below this point for prompting =============" in content
            content = content.split("# ============= remove below this point for prompting =============")[0].strip()
            seed_content.append(content)

    with open("seeds/common.py") as f:
        common_lib = f.read()

    common_lib_functions = extract_functions(common_lib)
    # Clean the common lib by removing any functions whose docstring begins/contains "internal function not used by LLM"
    common_lib_functions = [f for f in common_lib_functions if "internal function not used by LLM" not in f["docstring"]]
    common_lib_function_names = set([f["name"] for f in common_lib_functions])

    common_lib_classes = extract_class_definitions(common_lib)
    # Clean the common lib by removing any classes whose docstring begins/contains "internal class not used by LLM"
    common_lib_classes = [c for c in common_lib_classes if "internal class not used by LLM" not in c["docstring"]]

    common_lib = "\n\n".join([f["api_definition"] for f in common_lib_functions] + [c["api_definition"] for c in common_lib_classes])

    common_functions_calls_counter = {}
    concepts_in_seeds = []
    for content in seed_content:
        function_calls = extract_function_calls(content)
        common_functions_calls = common_lib_function_names.intersection(set(function_calls))

        for func in common_functions_calls:
            if func not in common_functions_calls_counter:
                common_functions_calls_counter[func] = 0
            common_functions_calls_counter[func] += 1

        # Extract the concepts, which come as a comment after the line containing "# concepts:"
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "# concepts:" in line:
                assert lines[i+1].startswith("# ")
                concepts = lines[i+1][2:].split(",")
                concepts = [c.strip() for c in concepts]
                concepts_in_seeds.extend(concepts)

    if False: # old prompt
        prompt = "The following code examples describe a function that generates a color grid input and a function that transforms the input grid to output grid. Later, the input and output grids will be given to students as puzzle. The puzzle is to figure out the rule that transforms the input grid to output grid. The puzzles should be interesting and challenging for students to solve. You will be creative and come up with similar and interesting problems. You can use the provided code examples as a reference to create your own problems."

        prompt += "\n\nCommon Library:\n\n```python\n" + common_lib + "\n```\n"

        prompt += "\nThe input generator function will be the function `generate_input`, and the transform function will be the function `main`.\n"

        for i in range(len(seed_content)):
            prompt += "\n\nExample:\n\n```python\n"+ seed_content[i] + "\n```\n"

        prompt += "\n\nFollowing the above format, your task is to create similar and interesting problems. You can use the provided code examples as a reference to create your own problems. Be sure to include the input generator function `generate_input` and the transform function `main` in your code examples in the same single code block."
        prompt += '\nMake use of the common library functions in your code examples. Come up with interesting visual or physic-inspired problems.'
    else:
        rng.shuffle(seed_content)
        examples = "\n\n".join([f"Example puzzle:\n```python\n{content}\n```" for content in seed_content])
        # remove "color change" from the concepts, because it is problematic and easily misinterpreted
        concepts_in_seeds = [c for c in concepts_in_seeds if c != "color change"]
        # deduplicate and randomly permute
        concepts_in_seeds = list(sorted(set(concepts_in_seeds)))
        rng.shuffle(concepts_in_seeds)
        concept_list = ", ".join(concepts_in_seeds)

        if remix == 0:
            remix1 = ""
            remix2 = ""
        elif remix == 1:
            remix1 = "in particular, making a new variation of the last example, by "
            remix2 = ", but remembering it should be a variation of the last example"
        else:
            remix1 = f"in particular, making a new variation of the last {remix} examples, by "
            remix2 = f", but remembering it should be a variation of the last {remix} examples"

        prompt = f"""You are a puzzle maker designing geometric and physical puzzles for curious middle-schoolers.

Each puzzle consists of discovery a deterministic rule, pattern, procedure, algorithm, or transformation law that maps inputs to outputs.
Both the inputs and outputs are 2D grids of colored pixels.

The middle schoolers are trying to discover this deterministic transformation, which can be implemented as a Python function called `main`.
Designing a puzzle involves also creating example inputs, which can be implemented as a Python function called `generate_input`. Unlike `main`, the `generate_input` function should be stochastic, so that every time you run it, you get another good example of what the transformation can be applied to.

Please design a single puzzle by writing code containing the `generate_input` and `main` functions. You can use the following standard library (`common.py`):
    
```python
{common_lib}
```

To give you ideas, here are some examples of other puzzles that middle schoolers enjoyed:
{examples}

Your task is to create a new puzzle that is similar to the examples provided, {remix1}following these steps:
1. First pick some `# concepts` from the example puzzles{remix2}. You can combine concepts from different examples. The concepts in the examples are:
   {concept_list}
2. Brainstorm a possible puzzle using those concepts, thinking of the physical/geometric/logical details
3. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts you chose and `# description:` describing the inputs and transformation.

Be sure to make the transformation `main` deterministic.
"""
        
    return prompt

if __name__ == "__main__":
    # get all files in seeds directory
    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]

    # print all files
    print("Used the following seeds:")
    for seed in seeds:
        print(seed)

    batch_size = 64
    remix_level = 2
    prompts = [ make_prompt(seeds, rng_seed, remix=remix_level) for rng_seed in range(batch_size) ]

    client = LLMClient()
    samples = []
    # use tqdm to go through the prompts and complete each of them
    from tqdm import tqdm
    for prompt in tqdm(prompts):
        samples.extend(client.generate(prompt, num_samples=1, max_tokens=1024*2, model=OpenAIModels.GPT_4_TURBO))
    
    codes = []
    for sample in samples:
        codes.extend(parse_code(sample))
    

    from utils import remove_trailing_code
    htmls = []

    common_functions_calls_counter = {}
    for code in codes:
        code = remove_trailing_code(code)
        # try:
        #     function_calls = extract_function_calls(code)
        #     # set intersection to find common function names
        #     common_functions_calls = common_lib_function_names.intersection(set(function_calls))
        # except:
        #     print("Error in extracting function calls")

        print(f"Code:\n{code}")
        # print(f"Funtion calls: {function_calls}")
        # print(f"Common functions calls: {common_functions_calls}")
        pwd = os.getcwd()
        global_vars = {}
        def execute_code(code, global_vars):
            exec(f"""{code}
examples_input_output = []
for _ in range(4):
    input_grid = generate_input()
    output_grid = main(input_grid)

    example = {{'input': input_grid, 'output': output_grid}}
    examples_input_output.append(example)
    #visualize(generate_input, main)
""", global_vars)

        try:
            func_timeout(5, execute_code, args=(code, global_vars))
        except FunctionTimedOut:
            print("Error: Code execution timed out after 10 seconds")
        except Exception as e:
            print("Error in executing code")
            print(f"Error: {e}")
        finally:
            os.chdir(pwd)

        if "examples_input_output" not in global_vars or len(global_vars["examples_input_output"]) <= 2:
            print("Error: Output not generated")
            continue

        from utils import generate_html_grid
        # an html string showing the Common Lib Function call names
        info_html = "" #f"""<div>Used Common Library Functions: {", ".join(list(common_functions_calls))}</div>"""
        grid_html = generate_html_grid(global_vars["examples_input_output"])
        # an html string showing the function calls in the code, use syntax highlighting
        # Syntax highlighting for the code
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter
        def highlight_code(code):
            formatter = HtmlFormatter()
            highlighted_code = highlight(code, PythonLexer(), formatter)
            style = f"<style>{formatter.get_style_defs('.highlight')}</style>"
            return style + highlighted_code
        code_html = highlight_code(code)
        htmls.append(grid_html + info_html + code_html)
        # for func in common_functions_calls:
        #     if func not in common_functions_calls_counter:
        #         common_functions_calls_counter[func] = 0
        #     common_functions_calls_counter[func] += 1   


# Combining everything into a final HTML
final_html = f"""
<html>
<head>
<title>Code Visualization</title>
</head>
<body>
{"<hr>".join(htmls)}
</body>
</html>
"""

with open(f"output_remix{remix_level}.html", "w") as f:
    f.write(final_html)