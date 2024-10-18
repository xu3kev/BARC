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
from seeds.common import *

def get_common_lib_from_file(file_path):
    """
    reference_code: a string containing the code that we are trying to use the common library to understand
    if it is provided then the only functions from the common_lib that are returned are the ones that are called in the reference_code
    """
    with open(file_path) as f:
        common_lib = f.read()
    
    common_lib_functions = extract_functions(common_lib)
    common_lib_functions = [f for f in common_lib_functions if "internal function not used by LLM" not in f["docstring"]]
    common_lib_function_names = set([f["name"] for f in common_lib_functions])

    common_lib_classes = extract_class_definitions(common_lib)
    # Clean the common lib by removing any classes whose docstring begins/contains "internal class not used by LLM"
    common_lib_classes = [c for c in common_lib_classes if "internal class not used by LLM" not in c["docstring"]]

    # common_lib = "\n\n".join([f["api_definition"] for f in common_lib_functions] + [c["api_definition"] for c in common_lib_classes])
    common_lib = (common_lib_classes, common_lib_functions)

    return common_lib, common_lib_function_names

def prune_common_lib(common_lib, reference_code):
    exceptions = ["Color"]
    called_functions = extract_function_calls(reference_code)
    called_functions = set(called_functions)
    common_lib_functions = common_lib[1]
    common_lib_function_names = set([f["name"] for f in common_lib_functions])
    called_common_lib_function_names = called_functions.intersection(common_lib_function_names)
    called_common_lib_functions = [f for f in common_lib_functions 
                                   if f["name"] in called_common_lib_function_names]
    called_common_lib_functions = [f for f in called_common_lib_functions]

    common_lib_classes = common_lib[0]
    # TODO: what's the best way to handle classes?
    # if `detect_rotational_symmetry`, `detect_translational_symmetry`, `detect_mirror_symmetry` is called, then we should include the Symmetry class
    symmetry_related_functions = ["detect_rotational_symmetry", "detect_translational_symmetry", "detect_mirror_symmetry"]
    symmetry_related_class_names = ["RotationalSymmetry", "TranslationalSymmetry", "MirrorSymmetry"]
    included_classes_names = exceptions + ["Symmetry"] if any([f in called_functions for f in symmetry_related_functions]) else exceptions
    for class_name in symmetry_related_class_names:
        if class_name in reference_code:
            if class_name not in included_classes_names:
                included_classes_names.append(class_name)

    called_common_lib_classes = [c for c in common_lib_classes if c["name"] in included_classes_names]
    
    called_common_lib = (called_common_lib_classes, called_common_lib_functions)

    return called_common_lib, called_common_lib_function_names

def make_self_instruct_prompt(seeds_contents, rng_seed, common_lib, common_lib_function_names,
                               brief_common=False, num_seeds=None, remix=0, library_function_hint=-1, uncreative=False, use_generator_prompt=True, hint_grid_size=0):
    """
    remix: how many example seeds the prompt tells the LLM to remix.
    0 means no remixing, just shows all the seeds. 1 tells it to remix one of the examples, 2 tells it to remix two of the examples, etc.
    """
    # make a random generator
    rng = random.Random(rng_seed)

    # Sort the seeds so that the order is consistent
    seeds_contents = list(sorted(seeds_contents, key=lambda x: x[0]))
    rng.shuffle(seeds_contents)
    if num_seeds is not None:
        seeds_contents = seeds_contents[:num_seeds]

    seed_content = []
    for _ , content in seeds_contents:
        assert "# ============= remove below this point for prompting =============" in content
        content = content.split("# ============= remove below this point for prompting =============")[0].strip()
        seed_content.append(content)

    if brief_common:
        common_lib, common_lib_function_names = prune_common_lib(common_lib, "\n".join(seed_content))

    # common_lib_functions = [f["api_definition"] for f in common_lib[1]]
    # common_lib_classes = [c["api_definition"] for c in common_lib[0]]
    # common_lib = list(set(common_lib_functions + common_lib_classes))
    common_lib_functions = common_lib[1]
    common_lib_classes = common_lib[0]
    common_lib = "\n\n".join([f["api_definition"] for f in common_lib_functions] + [c["api_definition"] for c in common_lib_classes])

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

    if uncreative:
        # Put special emphasis on the last puzzle
        examples = "\n\n".join([f"Example puzzle:\n```python\n{content}\n```" if seed_index < len(seed_content) - 1 else f"Example puzzle (last one, use it as a template!):\n```python\n{content}\n```"
                                for seed_index, content in enumerate(seed_content)])
    else:
        examples = "\n\n".join([f"Example puzzle:\n```python\n{content}\n```" for content in seed_content])
    # remove "color change" from the concepts, because it is problematic and easily misinterpreted
    concepts_in_seeds = [c for c in concepts_in_seeds if c != "color change"]
    # deduplicate and randomly permute
    concepts_in_seeds = list(sorted(set(concepts_in_seeds)))
    rng.shuffle(concepts_in_seeds)
    concept_list = ", ".join(concepts_in_seeds)

    if uncreative:
        assert remix == 1, "Lack of creativity requires exactly one problem to remix off of"

    if remix == 0:
        remix1 = ""
        remix2 = ""
    elif remix == 1:
        if uncreative:
            remix1 = "in particular, making a knock-off of the last example, by "
            remix2 = ", but remembering it should be a knock-off of the last example"
        else:
            remix1 = "in particular, making a new variation of the last example, by "
            remix2 = ", but remembering it should be a variation of the last example"
    else:
        if uncreative:
            remix1 = f"in particular, making a knock-off of the last {remix} examples, by "
            remix2 = f", but remembering it should be a knock-off of the last {remix} examples"
        else:
            remix1 = f"in particular, making a new variation of the last {remix} examples, by "
            remix2 = f", but remembering it should be a variation of the last {remix} examples"
    
    if library_function_hint == -1:
        library_function_hint_str = ""
    elif library_function_hint == 0:
        library_function_hint_str = "Make use of the common library functions."
    elif library_function_hint > 0:
        # select n random number of functions to hint at
        n = min(library_function_hint, len(common_lib_function_names))
        library_functions = rng.sample(list(common_lib_function_names), n)
        library_function_hint_str = f"Make use of the common library functions. In particular, use the function{'s' if library_function_hint > 1 else ''}: {', '.join(library_functions)}."

    if not uncreative: # creative
        # first part of the prompt just defines the problem, and introduces the common library, but without giving clear instructions on what examples should be considered
        prompt = f"""You are a puzzle maker designing geometric, physical, and topological puzzles for curious middle-schoolers.

Each puzzle consists of discovery a deterministic rule, pattern, procedure, algorithm, or transformation law that maps inputs to outputs.
Both the inputs and outputs are 2D grids of colored pixels. There are 10 colors, but the order of the colors is never relevant to the puzzle.

The middle schoolers are trying to discover this deterministic transformation, which can be implemented as a Python function called `main`.
Designing a puzzle involves also creating example inputs, which can be implemented as a Python function called `generate_input`. Unlike `main`, the `generate_input` function should be stochastic, so that every time you run it, you get another good example of what the transformation can be applied to.

Please design a single puzzle by writing code containing the `generate_input` and `main` functions. You can use the following standard library (`common.py`):
    
```python
{common_lib}
```
"""  
    # later parts of the prompt show examples and suggest how to combine them to make a new problem
    
        prompt += f"""
To give you ideas, here are some examples of other puzzles that middle schoolers enjoyed:

{examples}

Your task is to create a new puzzle that is similar to the examples provided, {remix1}following these steps:
1. First pick some `# concepts` from the example puzzles{remix2}. You can combine concepts from different examples. The concepts in the examples are:
   {concept_list}
"""
        if use_generator_prompt:
            prompt+="""2. Brainstorm a list of 20 concepts similar to the concept, thinking of the physical/geometric/topological/logical details
3. Pick one of the concepts from the brainstorming list, and create a new puzzle using that concept. To create a new puzzle:
4. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts you chose and `# description:` describing the inputs and transformation.
"""
        # this seemed to work okay:
        #3(a). Brainstorm what the input should look like. What are the objects, patterns, or structures that the middle schoolers should be looking at?
        #3(b). Brainstorm what the transformation should look like. How do the objects, patterns, or structures change in the output? What moves, changes, grows, shrinks, changes color, gets added, or gets removed?
        else:
            prompt+="""2. Brainstorm a possible puzzle using those concepts, thinking of the physical/geometric/topological/logical details
3. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts you chose and `# description:` describing the inputs and transformation.
"""
        # Gives some final instructions to try and ensure that things are done correctly
        prompt += f"""
Be sure to make the transformation `main` deterministic. Be sure to not assume or impose any ordering to the colors. Use physical, geometric, topological, and logical concepts.
"""
        
    else: # uncreative
        prompt = f"""You design knock-off puzzles by modifying the work of other puzzle designers just enough to avoid copyright infringement, because you aren't good at designing puzzles by yourself but need to make puzzles to make money.

Each puzzle consists of uncovering a single deterministic rule, pattern, procedure, algorithm, or general transformation that maps inputs to output. Both the inputs and outputs are 2D grids of colored pixels. There are 10 colors. The order of the colors is never relevant to the puzzle.

Your job is to create a knock-off puzzle that has similar concepts and challenges to puzzles created by honest puzzle makers. Be careful not to copy the work of another puzzler designer too closely, but make sure to follow the puzzle designers' techniques to make sure your knock-off puzzles are good.

Puzzle-solvers will try to figure out the deterministic transformation in the knock-off puzzle you create, which can be implemented as a Python function called `main`. Designing a knock-off puzzle involves creating example inputs, which can be implemented as a Python function called `generate_input`. Unlike `main`, the `generate_input` function should be stochastic, so that every time you run it, you get another good example grid that the transformation can be applied to.

Please create a single knock-off puzzle by writing code containing the `generate_input` and `main` functions. Please use the following standard library (`common.py`) as much as possible:

```python
{common_lib}
```

Here are some examples of good puzzles. These puzzles designed by good puzzle makers and your knock-off should rip them off:
{examples}

Your task is to create a knock-off puzzle that is based on the examples provided, {remix1}following these steps:

1. First pick some `# concepts` from the example puzzles{remix2}. You can combine concepts from different examples. The concepts in the examples are:
  {concept_list}
2. Brainstorm a knock-off using those concepts, paying special attention to the physical, geometric, topological, and logical details.
3. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts you chose and `# description:` describing the inputs and transformation.

Be sure to make the transformation `main` deterministic. Be especially sure to not assume or impose any ordering to the colors. Use physical, geometric, topological, and logical concepts as much as possible. Remember that the puzzle should be similar to the examples provided. Don't be creative. Try to emulate the puzzle makers you are ripping off. Remember you, yourself, are not good at making new puzzles but are very good at making knock-offs."""

    # Hint applies when either creative or uncreative
    if hint_grid_size:
        # hint at the grid size not too large but should not be a fixed number
        if not prompt[-1] == "\n":
            prompt += "\n"
        prompt += f"""Also, the input and output grids should not be too large, but should be large enough to contain interesting patterns. Both the width and heights of the grids should be under {hint_grid_size}."""
    
    if library_function_hint_str:
        prompt += f"""\n{library_function_hint_str}"""
    
    seeds = [seed for seed, _ in seeds_contents]
    return prompt, seeds

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--remix", "-r", type=int, default=1, help="how many example seeds to remix (can be 0)")
    parser.add_argument("--library_function_hint", "-l", type=int, default=-1, help="how many common library functions to hint at the end of the prompt")
    parser.add_argument("--batch_size", "-b", type=int, default=64, help="how many samples to draw")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--num_seeds", "-s", type=int, default=None, help="how many seeds to show in the prompt, if not all of them")
    parser.add_argument("--model", "-m", type=str, default="gpt-4-turbo", help="which model to use", 
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--sample_parallel", "-sp", type=int, default=1, help="how many parallel workers to use for sampling")
    parser.add_argument("--max_tokens", type=int, default=2048, help="max number of tokens for generation")
    parser.add_argument("--uncreative", "-u", action="store_true", help="use this flag to generate a prompt encourages less creativity, helpful for dumber LLMs", default=False)
    parser.add_argument("--brief_common", "-bc", action="store_true", help="use this flag to only include common library functions that are called in the examples", default=True)
    parser.add_argument("--generator_prompt", "-gp", action="store_true", help="use this flag to generate a list of concepts and have it pick one", default=False)
    parser.add_argument("--rng_offset", default=0, type=int)
    parser.add_argument("--nohtml", action="store_true", help="use this flag to not generate html", default=False)
    parser.add_argument("--hint_grid_size", default=0, type=int, help="use this flag to hint at the grid size")
    
    arguments = parser.parse_args()

    # convert model into enum
    for provider, model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if model.value == arguments.model:
            # should break on the correct values of model and provider, so we can use those variables later
            break

    # get all files in seeds directory
    # get current directory path
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    seeds = os.listdir(os.path.join(current_file_dir, "seeds"))
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    # get all files and its content
    seeds = [seed for seed in seeds if re.match(pattern, seed)]
    seeds_contents = []
    for seed in seeds:
        with open(os.path.join(current_file_dir, "seeds", seed)) as f:
            seeds_contents.append((seed, f.read()))

    # Load the common library
    common_lib, common_lib_function_names = get_common_lib_from_file(f"{current_file_dir}/seeds/common.py")

    # print all files
    print(f"Using the following {len(seeds)} seeds:", ", ".join(seeds).replace(".py", ""))
    # derive a offset from rng_seed_offset by hashing it if the rng_seed_orig is not 0
    from hashlib import md5
    if arguments.rng_offset != 0:
        rng_offset_str = md5(str(arguments.rng_offset).encode()).hexdigest()[:7]
        # to integer
        rng_offset = int(rng_offset_str, 16)
    else:
        rng_offset = 0
    batch_size = arguments.batch_size
    remix_level = arguments.remix
    library_function_hint = arguments.library_function_hint
    prompts_and_seeds = [ make_self_instruct_prompt(seeds_contents=seeds_contents, 
                                                    rng_seed=rng_seed + rng_offset, 
                                                    common_lib=common_lib,
                                                    common_lib_function_names=common_lib_function_names,
                                                    brief_common=arguments.brief_common, 
                                                    remix=remix_level, 
                                                    num_seeds=arguments.num_seeds,
                                                    library_function_hint=library_function_hint, 
                                                    uncreative=arguments.uncreative, 
                                                    use_generator_prompt=arguments.generator_prompt,
                                                    hint_grid_size=arguments.hint_grid_size)
               for rng_seed in tqdm(range(batch_size)) ]

    client = LLMClient(provider=provider, cache_dir=f"{current_file_dir}/cache")
    samples_and_seeds = []

    if arguments.sample_parallel == 1:
        for prompt, seed in tqdm(prompts_and_seeds):
            try:
                sample = client.generate(prompt, num_samples=1, max_tokens=arguments.max_tokens, temperature=arguments.temperature, model=model)[0]
                samples_and_seeds.append((sample, seed))        
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print("no samples, prompt was too big")
    else:
        just_the_prompts = [prompt for prompt, seed in prompts_and_seeds]
        list_of_lists_of_samples = client.generate_parallel(just_the_prompts, num_samples=1, max_tokens=arguments.max_tokens, num_workers=arguments.sample_parallel, model=model, temperature=arguments.temperature)
        # flatten the list
        samples = [sample for sublist in list_of_lists_of_samples for sample in sublist]
        samples_and_seeds = list(zip(samples, [seed for prompt, seed in prompts_and_seeds]))

    codes_and_seeds = []
    for sample, seeds in samples_and_seeds:
        parsed_codes = parse_code(sample)
        if parsed_codes:
            parsed_code = parsed_codes[0]
        else:
            parsed_code = ""
        codes_and_seeds.append((parsed_code, seeds))

    model_name = arguments.model.replace("/", "_")
    # write the codes to jsonl file
    file_name_base = f"self_instruct_remix{remix_level}_fewshot_{arguments.num_seeds}_{model_name}_temp{arguments.temperature:.2f}_maxtokens{arguments.max_tokens}_rng{arguments.rng_offset}"
    if arguments.uncreative:
        file_name_base += "_uncreative"
    if arguments.brief_common:
        file_name_base += "_briefcommon"
    if arguments.generator_prompt:
        file_name_base += "_generatorprompt"
    if arguments.hint_grid_size:
        file_name_base += f"_hintgridsize{arguments.hint_grid_size}"
    file_name_json = file_name_base + ".jsonl"
    print(f"Writing to jsonl {file_name_json}")
    with open(file_name_json, "w") as f:
        # jsonl, one json per line
        import json
        for code, seeds in codes_and_seeds:
            f.write(json.dumps({"code": code,
                                "seeds": seeds
                                }) + "\n")
    print(f"{len(codes_and_seeds)} codes written to {file_name_json}")
    
    if arguments.nohtml:
        exit()
    htmls = []

    common_functions_calls_counter = {}
    for code, seeds in codes_and_seeds:
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
        grid_html = generate_html_grid(examples_input_output, uid="None")
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
    file_name_html = file_name_base + ".html"

    print(f"Writing to {file_name_html}")
    with open(file_name_html, "w") as f:
        f.write(final_html)

if __name__ == "__main__":
    main()
