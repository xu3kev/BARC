import os
import re
import random
import numpy as np
from tqdm import tqdm

from utils import extract_functions, extract_function_calls, extract_class_definitions, parse_code, remove_trailing_code, generate_html_grid
from execution import execute_transformation, execute_input_generator
from llm import *

import sys
# add seeds/ to the python path
sys.path.append("seeds/")
from common import *

def get_common_lib_from_file(file_path="seeds/common.py"):
    with open(file_path) as f:
        common_lib = f.read()

    common_lib_functions = extract_functions(common_lib)
    # Clean the common lib by removing any functions whose docstring begins/contains "internal function not used by LLM"
    common_lib_functions = [f for f in common_lib_functions if "internal function not used by LLM" not in f["docstring"]]
    common_lib_function_names = set([f["name"] for f in common_lib_functions])

    common_lib_classes = extract_class_definitions(common_lib)
    # Clean the common lib by removing any classes whose docstring begins/contains "internal class not used by LLM"
    common_lib_classes = [c for c in common_lib_classes if "internal class not used by LLM" not in c["docstring"]]

    common_lib = "\n\n".join([f["api_definition"] for f in common_lib_functions] + [c["api_definition"] for c in common_lib_classes])
    return common_lib

def make_self_instruct_prompt(seeds, rng_seed, common_lib, num_seeds=None, remix=0):
    """
    remix: how many example seeds the prompt tells the LLM to remix.
    0 means no remixing, just shows all the seeds. 1 tells it to remix one of the examples, 2 tells it to remix two of the examples, etc.
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

    rng.shuffle(seed_content)
    if num_seeds is not None:
        seed_content = seed_content[:num_seeds]


    #common_functions_calls_counter = {}
    concepts_in_seeds = []
    for content in seed_content:
        # function_calls = extract_function_calls(content)
        # common_functions_calls = common_lib_function_names.intersection(set(function_calls))

        # for func in common_functions_calls:
        #     if func not in common_functions_calls_counter:
        #         common_functions_calls_counter[func] = 0
        #     common_functions_calls_counter[func] += 1

        # Extract the concepts, which come as a comment after the line containing "# concepts:"
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "# concepts:" in line:
                assert lines[i+1].startswith("# ")
                concepts = lines[i+1][2:].split(",")
                concepts = [c.strip() for c in concepts]
                concepts_in_seeds.extend(concepts)

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

    prompt = f"""You are a puzzle maker designing geometric, physical, and topological puzzles for curious middle-schoolers.

Each puzzle consists of discovery a deterministic rule, pattern, procedure, algorithm, or transformation law that maps inputs to outputs.
Both the inputs and outputs are 2D grids of colored pixels. There are 10 colors, but the order of the colors is never relevant to the puzzle.

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
2. Brainstorm a possible puzzle using those concepts, thinking of the physical/geometric/topological/logical details
3. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts you chose and `# description:` describing the inputs and transformation.

Be sure to make the transformation `main` deterministic. Be sure to not assume or impose any ordering to the colors. Use physical, geometric, topological, and logical concepts.
"""
        
    return prompt

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--remix", "-r", type=int, default=1, help="how many example seeds to remix (can be 0)")
    parser.add_argument("--batch_size", "-b", type=int, default=64, help="how many samples to draw")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--num_seeds", "-s", type=int, default=None, help="how many seeds to show in the prompt, if not all of them")
    parser.add_argument("--model", "-m", type=str, default="gpt-4-turbo", help="which model to use", 
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--sample_parallel", "-sp", type=int, default=1, help="how many parallel workers to use for sampling")
    
    arguments = parser.parse_args()

    # convert model into enum
    for provider, model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if model.value == arguments.model:
            # should break on the correct values of model and provider, so we can use those variables later
            break

    # get all files in seeds directory
    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]

    # print all files
    print(f"Using the following {len(seeds)} seeds:", ", ".join(seeds).replace(".py", ""))

    batch_size = arguments.batch_size
    remix_level = arguments.remix
    common_lib = get_common_lib_from_file("seeds/common.py")
    prompts = [ make_self_instruct_prompt(seeds, rng_seed, common_lib, remix=remix_level, num_seeds=arguments.num_seeds) for rng_seed in tqdm(range(batch_size)) ]

    client = LLMClient(provider=provider)
    samples = []
    # use tqdm to go through the prompts and complete each of them
    from tqdm import tqdm

    if arguments.sample_parallel == 1:
        for prompt in tqdm(prompts):
            samples.extend(client.generate(prompt, num_samples=1, max_tokens=1024*2, temperature=arguments.temperature, model=model))
    else:
        list_of_lists_of_samples = client.generate_parallel(prompts, num_samples=1, num_workers=arguments.sample_parallel, model=model, temperature=arguments.temperature)
        # flatten the list
        samples = [sample for sublist in list_of_lists_of_samples for sample in sublist]

    codes = []
    for sample in samples:
        codes.extend(parse_code(sample))
    
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

        input_grids = [ execute_input_generator(code) for _ in range(4)]
        # Filter out the grids that are not 2D arrays
        input_grids = [grid for grid in input_grids if isinstance(grid, np.ndarray) and len(grid.shape) == 2]
        print("Have", len(input_grids), "input grids")
        output_grids = [ execute_transformation(code, grid) for grid in input_grids]
        print("Have", len(output_grids), "output grids")
        examples_input_output = [ {"input": input_grid, "output": output_grid}
                                    for input_grid, output_grid in zip(input_grids, output_grids) 
                                    if isinstance(output_grid, np.ndarray) ]
        if len(examples_input_output) == 0:
            print("Bad code")
            continue        

        # an html string showing the Common Lib Function call names
        info_html = "" #f"""<div>Used Common Library Functions: {", ".join(list(common_functions_calls))}</div>"""
        grid_html = generate_html_grid(examples_input_output)
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
    file_name = f"self_instruct_remix{remix_level}_{arguments.num_seeds}_{arguments.model}_temp{arguments.temperature:.2f}.html"

    print(f"Writing to {file_name}")
    with open(file_name, "w") as f:
        f.write(final_html)