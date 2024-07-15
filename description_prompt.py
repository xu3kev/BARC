import os
import re
import random
from tqdm import tqdm
from utils import get_description_from_lines, get_concepts_from_lines

from llm import *

# add seeds/ to the python path
from seeds.common import *

def extract_concepts_and_descriptions(content):
    lines = content.split("\n")

    best_solution_line = None
    # find the line containing "BEST SOLUTION"
    for i, line in enumerate(lines):
        if "SOLUTION PICK" in line:
            best_solution_line = i
            break
    
    lines = lines[best_solution_line:]

    # Extract the concepts, which come as a comment after the line containing "# concepts:"
    concepts = get_concepts_from_lines(lines)
    
    # Extract the descriptions, which come as a comment after the line containing "# description:"
    description = get_description_from_lines(lines)
    return concepts, description


def make_self_instruct_prompt(seeds_contents, rng_seed, num_descriptions=None, use_concepts=True):
    # make a random generator
    rng = random.Random(rng_seed)

    # Sort the seeds so that the order is consistent
    seeds_contents = list(sorted(seeds_contents, key=lambda x: x[0]))
    rng.shuffle(seeds_contents)
    if num_descriptions is not None:
        seeds_contents = seeds_contents[:num_descriptions]

    seed_content = []
    for _ , content in seeds_contents:
        assert "# ============= remove below this point for prompting =============" in content
        content = content.split("# ============= remove below this point for prompting =============")[0].strip()
        seed_content.append(content)

    concepts_and_descriptions_in_seeds = []
    for content in seed_content:
        concepts, description = extract_concepts_and_descriptions(content)

        # remove "color change" from the concepts, because it is problematic and easily misinterpreted
        concepts = [c for c in concepts if c != "color change"]
        # deduplicate and randomly permute
        concepts = list(sorted(set(concepts)))
        rng.shuffle(concepts)
        concept_list = ", ".join(concepts)
        
        concepts_and_descriptions_in_seeds.append((concept_list, description))

    if use_concepts:
        examples = "\n\n".join([f"Example puzzle concepts and description:\n```python\n# concepts:\n# {concept_list}\n# description:\n# {description}\n```" for concept_list, description in concepts_and_descriptions_in_seeds])
    else:
        examples = "\n\n".join([f"Example puzzle description:\n```python\n# description:\n# {description}\n```" for concept_list, description in concepts_and_descriptions_in_seeds])

    # read the prompt template from prompts/description_prompt.md
    with open("prompts/description_prompt.md") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(examples=examples)
    print(prompt)
    seeds = [seed for seed, _ in seeds_contents]
    return prompt, seeds

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")

    parser.add_argument("--num_descriptions", "-d", type=int, default=None, help="how many descriptions to show in the prompt, if not all of them")
    parser.add_argument("--num_samples", "-ns", type=int, default=1, help="how many description to sample from a single prompt")
    parser.add_argument("--batch_size", "-b", type=int, default=64, help="how many batches of descriptions to generate")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--model", "-m", type=str, default="gpt-4-turbo", help="which model to use", 
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--sample_parallel", "-sp", type=int, default=1, help="how many parallel workers to use for sampling")
    parser.add_argument("--max_tokens", type=int, default=2048, help="max number of tokens for generation")
    parser.add_argument("--rng_offset", type=int, default=0, help="offset to rng_seed_offset")
    parser.add_argument("--use_concepts", "-uc", action="store_false", help="use concepts in the prompt", default=True)
    
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
    prompts_and_seeds = [ make_self_instruct_prompt(seeds_contents=seeds_contents, 
                                                    rng_seed=rng_seed + rng_offset, 
                                                    num_descriptions=arguments.num_descriptions,
                                                    use_concepts=arguments.use_concepts)
               for rng_seed in tqdm(range(batch_size)) ]

    client = LLMClient(provider=provider, cache_dir=f"{current_file_dir}/cache")
    samples_and_seeds = []

    if arguments.sample_parallel == 1:
        for prompt, seed in tqdm(prompts_and_seeds):
            try:
                sample = client.generate(prompt, num_samples=arguments.num_samples, max_tokens=arguments.max_tokens, temperature=arguments.temperature, model=model)[0]
                samples_and_seeds.append((sample, seed))        
            except:
                print("no samples, prompt was too big")
    else:
        just_the_prompts = [prompt for prompt, seed in prompts_and_seeds]
        list_of_lists_of_samples = client.generate_parallel(just_the_prompts, num_samples=arguments.num_samples, max_tokens=arguments.max_tokens, num_workers=arguments.sample_parallel, model=model, temperature=arguments.temperature)
        # flatten the list
        samples = [sample for sublist in list_of_lists_of_samples for sample in sublist]
        samples_and_seeds = list(zip(samples, [seed for prompt, seed in prompts_and_seeds]))

    concepts_description_and_seeds = []
    for sample, seeds in samples_and_seeds:
        print(f"sample: {sample}")
        parsed_concepts, parsed_description = extract_concepts_and_descriptions(sample)
        parsed_concepts = ", ".join(parsed_concepts)
        concepts_description_and_seeds.append((parsed_concepts, parsed_description, seeds))

    model_name = arguments.model.replace("/", "_")
    # write the codes to jsonl file
    file_name_base = f"self_instruct_descriptions_fewshot_{arguments.num_descriptions}_{model_name}_temp{arguments.temperature:.2f}_maxtokens{arguments.max_tokens}_rng{arguments.rng_offset}"
    if arguments.use_concepts:
        file_name_base += "_concepts"
    file_name_json = file_name_base + ".jsonl"
    print(f"Writing to jsonl {file_name_json}")
    with open(file_name_json, "w") as f:
        # jsonl, one json per line
        import json
        for concepts, description, seeds in concepts_description_and_seeds:
            f.write(json.dumps({"concepts": concepts,
                                "description": description,
                                "seeds": seeds
                                }) + "\n")
    print(f"{len(concepts_description_and_seeds)} codes written to {file_name_json}")

if __name__ == "__main__":
    main()