from arc import train_problems
import os
import importlib

import sys
# add seeds/ to the python path so we can import common
sys.path.append("seeds/")
from common import *

import numpy as np


def validate(problem):
    # copy the file to temporary_validation.py
    os.system(f"cp seeds/{problem.uid}.py temporary_validation.py")

    # execute everything in temporary_validation.py, which is going to define a function called `main`
    # important that we are able to call this function here
    spec = importlib.util.spec_from_file_location("temporary_validation", "temporary_validation.py")
    temporary_validation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temporary_validation)

    failure = False

    for train_pair in problem.train_pairs + problem.test_pairs:
        # transpose the input and output grids, because we index them x,y and they are stored as r,c
        input_grid = train_pair.x.T
        expected_output_grid = train_pair.y.T

        try:
            output_grid = temporary_validation.main(input_grid)
        except Exception as e:
            print(f'Validation failure on {problem.uid}')
            print('Input:')
            show_colored_grid(input_grid)
            print('Expected output:')
            show_colored_grid(expected_output_grid)
            print('Error:')
            print(e)
            print()
            failure = True
            continue

        if not np.array_equal(output_grid, expected_output_grid):
            print(f'Validation failure on {problem.uid}')
            print('Input:')
            show_colored_grid(input_grid)
            print('Expected output:')
            show_colored_grid(expected_output_grid)
            print('Actual output:')
            show_colored_grid(output_grid)
            print()
            failure = True

    # cleanup
    os.system("rm temporary_validation.py")

    if not failure: print(f"\t[+] passed")

    return not failure


no_seed_provided, validation_passed, validation_failed = 0, [], []
for problem in train_problems:
    if len(sys.argv) > 1 and problem.uid not in sys.argv[1:]:
        continue
    
    # check if we have a manually constructed seed solution to this problem
    if not os.path.exists(f"seeds/{problem.uid}.py"):
        no_seed_provided += 1
        continue

    print(f"Validating {problem.uid}...")

    if validate(problem):
        validation_passed.append(problem.uid)
    else:
        validation_failed.append(problem.uid)

print(f"Have seeds for {len(train_problems) - no_seed_provided}/{len(train_problems)} problems")
print(f"Validation passed for {len(validation_passed)}/{len(train_problems) - no_seed_provided} problems")
print(f"Validation failed for {len(validation_failed)}/{len(train_problems) - no_seed_provided} problems")
print("\nPassing problems: ", " ".join(validation_passed))
print("\nFailing problems: ", " ".join(validation_failed))