# Boostrapping ARC: Synthetic Problem Generation for ARC-AGI Visual Reasoning Tasks

# Seed problems

The seed problems are manually written "solution" and "input_generator" for the problems in ARC training set.

* solution: including natural language description and the `main` funciton (solution to the task) which takes the input grid and transform it to the output grid which solves the problem.
* input_generator: The `generate_input` function generates input grids that resemebles the input grids of the corresponding problem.

There are currently 162 solutions/input_generators under `seeds/` folder.

# Synthetic Data Generation

The synthetic data generation pipeline takes the seed problems, remix them with LLM to generate new problems including both the "solution" and "input_generator". Then we instantiate the synthetic ARC problem by execute input_generator to create input grids, and solution to create the corresponding output grids to create a list of input/output pairs as the ARC problem.

The synthetic data generation consist of 3 stages.

* description generations: generate the natural language description of synthetic problems given the manual written descriptions. See `generate_descriptions.py `
* code generation: generate the solution and input generation code given the description and similar few-shot examples from seeds (by RAG). See `generate_code.py`
* problem generation: execute the generated code to instantiate the concrete ARC problems. See `generate_problems.py`

Please refer to `data_generation_script.sh` for example usage.

# Finetuning

We use the framework from huggingface-alignmenthandbook.


# Inference

# 

# Viewing ARC problems

ARC interface hosted by Wen-Ding: [https://www.cs.cornell.edu/~wdli/arc_interface/](https://www.cs.cornell.edu/~wdli/arc_interface/)

You can view ARC problems by their ID number using the `view_problem.py` script. For example:
```bash
$ python view_problem.py 09629e4f
```
You will see both a textual representation (as grids of numbers), as well as a graphical representation (using matplotlib).

You can also visit [MC-LARC](https://mc-larc.github.io/) for a more interactive interface.


# Solving problems

Your solutions to ARC problems should be under `seeds/` and should consist of a Python file with the ID of the problem.
For instance, one such file is `seeds/05f2a901.py`, which contains a seed solution to `05f2a901`.

Keep track of which problems you are solving so that you do not overlap with others. The tracking spreadsheet is [https://docs.google.com/spreadsheets/d/1uPeAawNicITtLnT2aEclD5Ee-47gnfdXjuzugtfqceM/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1uPeAawNicITtLnT2aEclD5Ee-47gnfdXjuzugtfqceM/edit?usp=sharing)


Seed files should be of this form:
```python
from common import *

import numpy as np
from typing import *

# concepts:
# <list of concepts, separated by commas>

# description:
# <a couple sentences describing how to solve the problem, including what you'll see in the input>

def main(input_grid):
    ... # computes the output grid from the input

def generate_input():
    ... # returns a random input grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
```

# Prior knowledge

Common subroutines that are important to multiple ARC problems should go in `seeds/common.py`.
