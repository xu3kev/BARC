# Installation

The only nonstandard library that you'll need is `arc-py`:
```bash
$ python -m pip install arc-py
```

# Viewing ARC problems

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