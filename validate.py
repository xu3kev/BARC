from arc import train_problems, validation_problems
from conceptarc import concept_arc_problems
import os

from execution import execute_transformation

import numpy as np

import sys
sys.path.append("seeds/")
from common import *


def validate(problem):
    # load the source code
    with open(f"seeds/{problem.uid}.py") as f:
        source = f.read()

    failure = False

    for train_pair in problem.train_pairs + problem.test_pairs:
        if failure: break
        # transpose the input and output grids, because we index them x,y and they are stored as r,c
        input_grid = train_pair.x.T
        expected_output_grid = train_pair.y.T

        output_grid = execute_transformation(source, input_grid,
                                             timeout=None if len(sys.argv) > 1 else 1) # no timeout when debugging a single problem

        if isinstance(output_grid, str):
            print(f'Validation failure on {problem.uid}')
            print('Input:')
            show_colored_grid(input_grid)
            print('Expected output:')
            show_colored_grid(expected_output_grid)
            print('Error:')
            print(output_grid)
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

    if not failure: print(f"\t[+] passed")

    return not failure


no_seed_provided, validation_passed, validation_failed = 0, [], []
for problem in train_problems + validation_problems + concept_arc_problems():
    if len(sys.argv) > 1 and not any( problem.uid.startswith(prefix) for prefix in sys.argv[1:]):
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
