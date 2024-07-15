import os
import re
import random
from tqdm import tqdm
import numpy as np

from utils import extract_functions, extract_function_calls, extract_class_definitions, parse_code, remove_trailing_code, generate_html_grid, get_description_from_lines, get_concepts_from_lines
from execution import execute_transformation, execute_input_generator

from llm import *

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
    symmtry_related_functions = ["detect_rotational_symmetry", "detect_translational_symmetry", "detect_mirror_symmetry"]
    included_classes_names = exceptions + ["Symmetry"] if any([f in called_functions for f in symmtry_related_functions]) else exceptions
    called_common_lib_classes = [c for c in common_lib_classes if c["name"] in included_classes_names]
    
    called_common_lib = (called_common_lib_classes, called_common_lib_functions)

    return called_common_lib, called_common_lib_function_names

def extract_concepts_and_descriptions(content):
    lines = content.split("\n")

    # Extract the concepts, which come as a comment after the line containing "# concepts:"
    concepts = get_concepts_from_lines(lines)
    
    # Extract the descriptions, which come as a comment after the line containing "# description:"
    description = get_description_from_lines(lines)
    
    return concepts, description

def make_self_instruct_prompt(seeds_content_and_embedding, problem_concept, problem_description, problem_embedding, num_seeds=1, common_lib=None, common_lib_function_names=None, brief_common=True):
    seed_embeddings = [embedding for _, _, embedding in seeds_content_and_embedding]
    A = np.array(seed_embeddings)
    B = np.array(problem_embedding)

    cosine = np.dot(A,B)/(np.linalg.norm(A, axis=1)*np.linalg.norm(B))
    most_similar_order = np.argsort(cosine)[::-1]

    ordered_seeds_content_and_embedding = [seeds_content_and_embedding[i] for i in most_similar_order]

    best_seeds_content_and_embedding = ordered_seeds_content_and_embedding[:num_seeds]

    seed_content = [content for _, content, _ in best_seeds_content_and_embedding]

    examples = "\n\n".join([f"Example puzzle code:\n```python\n{content}\n```" for content in seed_content])

    if brief_common:
        common_lib, common_lib_function_names = prune_common_lib(common_lib, "\n".join(seed_content))

    common_lib_functions = common_lib[1]
    common_lib_classes = common_lib[0]
    common_lib = "\n\n".join([f["api_definition"] for f in common_lib_functions] + [c["api_definition"] for c in common_lib_classes])

    description = f"Concepts: \n{problem_concept}\n\nDescription: \n{problem_description}"

    # read the prompt template from prompts/problem_from_description.md
    with open("prompts/problem_from_description.md") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(description=description, common_lib=common_lib, examples=examples)
    print(prompt)
    seeds = [seed for seed, _, _ in best_seeds_content_and_embedding]
    return prompt, seeds

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--jsonl", type=str, default=None, help="jsonl file descriptions to use in prompts")
    parser.add_argument("--num_seeds", "-s", type=int, default=1, help="how many seeds to show in the prompt, if more than 1")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--prompt_model", "-pm", type=str, default="gpt-4-turbo", help="which model to use for problem generation", 
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--embedding_model", "-em", type=str, default="text-embedding-ada-002", help="which model to use for embedding",
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--sample_parallel", "-sp", type=int, default=1, help="how many parallel workers to use for sampling")
    parser.add_argument("--max_tokens", type=int, default=2048, help="max number of tokens for generation")
    parser.add_argument("--brief_common", "-bc", action="store_true", help="only include common functions that are called in the seed code", default=True)
    parser.add_argument("--nohtml", action="store_true", help="don't generate html", default=False)
    
    arguments = parser.parse_args()

    # convert prompt model into enum
    for prompt_provider, prompt_model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if prompt_model.value == arguments.prompt_model:
            # should break on the correct values of prompt_model and prompt_provider, so we can use those variables later
            break
        
    # convert embedding model into enum
    for embedding_provider, embedding_model in [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list]:
        if embedding_model.value == arguments.embedding_model:
            # should break on the correct values of embedding_model and embedding_provider, so we can use those variables later
            break

    import json
    problem_concepts = []
    problem_descriptions = []
    problem_seeds = []
    # read the jsonl file
    print(f"Reading from {arguments.jsonl}")
    result_saving_file = arguments.jsonl.replace(".jsonl", "_generated_problems.jsonl")
    print(f"Saving to {result_saving_file}")
    with open(arguments.jsonl) as f:
        data = f.readlines()
    for line in data:
        problem = json.loads(line)
        problem_concepts.append(problem["concepts"])
        problem_descriptions.append(problem["description"])
        problem_seeds.append(problem["seeds"])
    
    # get current directory path
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    seeds = os.listdir(os.path.join(current_file_dir, "seeds"))
    
    # generate embedding for the problem descriptions
    client = LLMClient(provider=embedding_provider, cache_dir=f"{current_file_dir}/cache")
    problem_embeddings = [client.generate_embedding(description, model=embedding_model) for description in problem_descriptions]
        

    # get all files in seeds directory
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    # get all files and its content
    seeds = [seed for seed in seeds if re.match(pattern, seed)]
    seeds_contents = []
    for seed in seeds:
        with open(os.path.join(current_file_dir, "seeds", seed)) as f:
            seeds_contents.append((seed, f.read()))

    seed_content = []
    for seed , content in seeds_contents:
        assert "# ============= remove below this point for prompting =============" in content
        content = content.split("# ============= remove below this point for prompting =============")[0].strip()
        seed_content.append((seed, content))

    seeds_content_and_embedding = []
    for seed, content in seed_content:
        _, description = extract_concepts_and_descriptions(content)

        # generate embedding for this seed
        embedding = client.generate_embedding(description, model=embedding_model)
        seeds_content_and_embedding.append((seed, content, embedding))
    
    # Load the common library
    common_lib, common_lib_function_names = get_common_lib_from_file(f"{current_file_dir}/seeds/common.py")

    # print all files
    print(f"Using the following {len(seeds)} seeds:", ", ".join(seeds).replace(".py", ""))
    prompts_and_seeds = [ make_self_instruct_prompt(seeds_content_and_embedding=seeds_content_and_embedding, 
                                                    problem_concept=problem_concept, 
                                                    problem_description=problem_description, 
                                                    problem_embedding=problem_embedding, 
                                                    num_seeds=arguments.num_seeds,
                                                    common_lib=common_lib,
                                                    common_lib_function_names=common_lib_function_names,
                                                    brief_common=arguments.brief_common)
               for problem_concept, problem_description, problem_embedding in tqdm(zip(problem_concepts, problem_descriptions, problem_embeddings)) ]

    client = LLMClient(provider=prompt_provider, cache_dir=f"{current_file_dir}/cache")
    samples_and_seeds = []
    if arguments.sample_parallel == 1:
        for prompt, seed in tqdm(prompts_and_seeds):
            try:
                sample = client.generate(prompt, num_samples=1, max_tokens=arguments.max_tokens, temperature=arguments.temperature, model=prompt_model)[0]
                samples_and_seeds.append((sample, seed))        
            except Exception as e:
                print(f"error occurred: {e}")
    else:
        just_the_prompts = [prompt for prompt, seed in prompts_and_seeds]
        list_of_lists_of_samples = client.generate_parallel(just_the_prompts, num_samples=1, max_tokens=arguments.max_tokens, num_workers=arguments.sample_parallel, model=prompt_model, temperature=arguments.temperature)
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

    prompt_model_name = arguments.prompt_model.replace("/", "_")
    # write the codes to jsonl file
    file_name_base = f"self_instruct_code_fewshot_{arguments.num_seeds}_{prompt_model_name}_temp{arguments.temperature:.2f}_maxtokens{arguments.max_tokens}"
    if arguments.brief_common:
        file_name_base += "_briefcommon"
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
        print(f"Code:\n{code}")

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
