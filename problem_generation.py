import argparse
import random
from execution import multi_execute_transformation, multi_execute_input_generator, execute_transformation
import numpy as np
import os
import re
import tqdm
import json
import time

class Problem:
    def __init__(self, source_code):
        self.source = source_code
        self.examples = []
        self.seeds = []
        

    def add_example(self, input_grid, output_grid):
        self.examples.append((input_grid, output_grid))
    def to_dict(self):
        return {
            "source": self.source,
            "examples": [(input_grid.tolist(), output_grid.tolist()) for input_grid, output_grid in self.examples],
            "seeds": self.seeds
        }


def check_grid(grid):
    # check the grid is well-formed, 2d numpy array of integers between 0-9
    try:
        assert isinstance(grid, np.ndarray)
        assert len(grid.shape) == 2
        assert grid.shape[0] > 0 and grid.shape[1] > 0
        assert np.all((0 <= grid) & (grid <= 9))
    except AssertionError:
        return False
    return True

def check_grids_all_equal(grids):
    """check a set of grids are all equal"""
    assert len(grids) > 0
    return all(np.array_equal(grids[0], grid) for grid in grids)

def check_diversity(grids, threshold):
    """check a set of grids is diverse, i.e. the grids should be sufficiently different from each other"""
    # TODO
    pass

def check_identity(input_grid, output_grid):
    try:
        assert check_grid(input_grid)
        assert check_grid(output_grid)
    except:
        breakpoint()
    return np.array_equal(input_grid, output_grid)

def generate_input_grids(problem_source, num_returns=3, timeout=1, function_name="generate_input", retries=20, deduplicate=True):
    """
    given a problem source code, generate an input grid
    """
    random.seed(0)

    return_input_grids = []
    tries = 0
    BATCH_SIZE = num_returns
    while len(return_input_grids) < num_returns and tries < retries:
        random_seeds = [random.randint(0, 1<<30) for _ in range(BATCH_SIZE)]
        input_grids = multi_execute_input_generator([problem_source] * BATCH_SIZE, random_seeds, timeout, function_name)
        for input_grid in input_grids:
            if not check_grid(input_grid):
                tries += 1
                print('Non well-formed input grid')
                continue
            if deduplicate and any(np.array_equal(input_grid, existing_grid) for existing_grid in return_input_grids):
                tries += 1
                print('Duplicate input grid')
                continue
            return_input_grids.append(input_grid)

    return return_input_grids

def get_random_color_mapping(only_non_black=True, permute_colors=None):
    """
    Get a random color mapping from 0-9 to 0-9 where 0 is black.
    If only_non_black is True, map 1-9 to 1-9.
    """
    if permute_colors is None:
        permute_colors = list(range(10))
    else:
        permute_colors = sorted(permute_colors)

    if only_non_black:
        if 0 in permute_colors:
            permute_colors.remove(0)

    shuffled_colors = list(permute_colors)
    random.shuffle(shuffled_colors)
    color_mapping = dict(zip(permute_colors, shuffled_colors))
    # add the rest of the colors as identity mapping
    for i in range(10):
        if i not in color_mapping:
            color_mapping[i] = i
    
    return color_mapping

def apply_color_mapping(grid, color_mapping):
    """
    Apply a color mapping to the grid
    """
    return np.vectorize(color_mapping.get)(grid)

def add_color_changing_code(problem_source, color_mapping=None):
    if color_mapping is None:
        color_mapping = {i: i for i in range(10)}
    color_code = f"""
Color.BLACK = {color_mapping[0]}
Color.BLUE = {color_mapping[1]}
Color.RED = {color_mapping[2]}
Color.GREEN = {color_mapping[3]}
Color.YELLOW = {color_mapping[4]}
Color.GREY = {color_mapping[5]}
Color.GRAY = {color_mapping[5]}
Color.PINK = {color_mapping[6]}
Color.ORANGE = {color_mapping[7]}
Color.TEAL = {color_mapping[8]}
Color.MAROON = {color_mapping[9]}
"""
    # Split the source code into lines
    lines = problem_source.split('\n')

    # Find the last line of the imports
    import_end_index = 0
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from"):
            import_end_index = i + 1

    # Insert the color_code after the imports
    lines.insert(import_end_index, color_code)

    # Join the lines back into a single string
    modified_source = '\n'.join(lines)

    return modified_source

def run_transformation(source, input_grid, timeout=1, function_name="main", num_returns=50):
    """
    run the transformation on the input grid and return the output grid multiple times
    """
    random.seed(0)
    random_seeds = [random.randint(0, 1<<30) for _ in range(num_returns)]
    output_grids = multi_execute_transformation([source] * num_returns, [input_grid] * num_returns, random_seeds, timeout, function_name)
    return output_grids

def generate_problem(problem_source, num_input_grids=30, num_deterministic_check=20, num_color_permute_check=20, timeout=1, total_timeout=30):
    """
    Generate a problem by generating input grids and running the transformation on them.
    Return None for the problem if:
    1. non-deterministic transformations
    2. non color-invariant transformations

    For the example input-output grid pair, remove for the example pair if:
    1. input grid is the same as the output grid
    """
    start = time.time()
    problem = Problem(problem_source)

    input_grids = generate_input_grids(problem_source, num_returns=num_input_grids, timeout=timeout, deduplicate=True)
    random.seed(0)

    # Check for non-deterministic transformations
    for input_grid in input_grids:
        if time.time() - start > total_timeout:
            print(f"Total timeout reached after {total_timeout} seconds")
            return None
        output_grids = run_transformation(problem_source, input_grid, timeout=timeout, num_returns=num_deterministic_check)
        if len(output_grids) == 0:
            print("No output grids")
            continue
        if not check_grids_all_equal(output_grids):
            print("Non-deterministic transformation")
            return None
        if not all(check_grid(output_grid) for output_grid in output_grids):
            # if any of the output grids are not well-formed, skip this particular input grid
            print('Non well-formed output grid, skipping this input grid')
            continue
        if np.all(output_grids[0] == 0):
            print("Output grid is entirely black, skipping this example")
            continue

        expected_output_grids = output_grids[0]

        # Check for non-color-invariant transformations
        permuted_input_grids = []
        modified_problem_sources = []
        color_mappings = []
        for _ in range(num_color_permute_check):
            color_mapping = get_random_color_mapping(only_non_black=True)
            color_mappings.append(color_mapping)
            permuted_input_grid = apply_color_mapping(input_grid, color_mapping)
            permuted_input_grids.append(permuted_input_grid)
            modified_problem_source = add_color_changing_code(problem_source, color_mapping)
            modified_problem_sources.append(modified_problem_source)

        random_seeds = [random.randint(0, 1<<30) for _ in range(num_color_permute_check)]
        permuted_output_grids = multi_execute_transformation(modified_problem_sources, 
                                                             permuted_input_grids, random_seeds, timeout, function_name="main")

        if len(permuted_output_grids) != num_color_permute_check:
            print("some transformations failed during permute check")
            return None
        for permuted_output_grid, color_mapping in zip(permuted_output_grids, color_mappings):
            if not check_grid(permuted_output_grid) or not check_grid(input_grid):
                print("Permute check failed due to non-well-formed grids")
                return None
            if not check_identity(apply_color_mapping(expected_output_grids, color_mapping), permuted_output_grid):
                print("Permute check failed")
                return None

        output_grid = execute_transformation(problem_source, input_grid, timeout, function_name="main")
        if check_identity(input_grid, output_grid):
            print("Identity transformation, skipping this example")
            continue
        problem.add_example(input_grid, output_grid)

    return problem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", type=str, help="Path to jsonl file containing program generation")
    parser.add_argument("--problem_source_uid", type=str, help="Problem id of a seed problem to validate")
    parser.add_argument("--run_all_seed", action="store_true", help="Run all seed problems")
    parser.add_argument("--py_file", type=str, help="Path to the python file containing the problem")
    args = parser.parse_args()

    # only one of problem_uid or run_all_seed or jsonl should be provided
    assert sum([args.problem_source_uid is not None, args.run_all_seed, args.jsonl is not None,
                args.py_file is not None]) == 1, "Provide one of problem_uid, run_all_seed or jsonl"

    problems_source = []
    problems_seeds = []
    problem_source_uids = []
    if args.problem_source_uid:
        problem_source_uids = [args.problem_source_uid]
    elif args.run_all_seed:
        seeds = os.listdir("seeds")
        # filter files with .py extension and 8 hex value characters in the file name
        pattern = r"([0-9a-f]{8})\.py"
        problem_source_uids = [re.match(pattern, filename).group(1) for filename in seeds if re.match(pattern, filename)]
        # Now `matched_files` contains all the filenames that match the pattern
    elif args.jsonl:
        print(f"Reading from {args.jsonl}")
        result_saving_file = args.jsonl.replace(".jsonl", "_generated_problems.jsonl")
        print(f"Saving to {result_saving_file}")
        with open(args.jsonl) as f:
            data = f.readlines()
        for line in data:
            problem = json.loads(line)
            problems_source.append(problem["code"])
            problems_seeds.append(problem["seeds"])
    elif args.py_file:
        with open(args.py_file) as f:
            source = f.read()
        problems_source.append(source)
    else:
        raise ValueError("Provide one of problem_uid, run_all_seed or jsonl")

    if problem_source_uids:
        for problem_source_uid in problem_source_uids:
            with open(f"seeds/{problem_source_uid}.py") as f:
                source = f.read()
            problems_source.append(source)


    problems = []
    for i, problem_source in enumerate(tqdm.tqdm(problems_source)):
        problem = generate_problem(problem_source, total_timeout=30)
        if problem and len(problem.examples) >= 4:
            print(f"+1 problem with {len(problem.examples)} examples")
            if args.jsonl:
                problem.seeds = problems_seeds[i]
            problems.append(problem)
        else:
            if problem_source_uids:
                print(f"Problem {problem_source_uids[i]} is not valid")
        print(f"so far, generated {len(problems)} problems")

    # write list of Problem to jsonl file
    print(f'Generated {len(problems)} problems')
    if args.jsonl:
        with open(result_saving_file, "w") as f:
            for problem in problems:
                f.write(json.dumps(problem.to_dict()) + "\n")


if __name__ == "__main__":
    main()