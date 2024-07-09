You are a programmer writing code to transform grids of colored pixels. You have a common library (`common.py`) of utility functions.
You have written a function called `main` that does an interesting transformation, but it is getting too long and complicated. You want to refactor `main` into subroutines.
Each subroutine should draw just part of the output grid by returning a tuple of a color grid (np array), and a background/transparent color indicating which color shouldn't be copied into the final output.
Each subroutine only gets to look at the input grid.

Here is the common utility library:
```python
# common.py
{common}
```

Here is the original `main` function that you are going to refactor into subroutines, each drawing just some of the output:
```python
{original}
```

Here is the template that you should use for your refactoring:
```python
# Follow this template
from common import *
import numpy as np

def main(input_grid):
    # <comment describing the first subset of the things that are combined to produce the output>
    output_1, background_transparent_1 = make_part_of_output_1(input_grid)
    # <comment describing the second subset of the things that are combined to produce the output>
    output_2, background_transparent_2 = make_part_of_output_2(input_grid)
    # ... do as many as needed, but you might not need so many ...

    final_output = np.zeros_like(output_1)
    final_output[output_1 != background_transparent_1] = output_1[background_transparent_1]
    final_output[output_2 != background_transparent_2] = output_2[output_2 != background_transparent_2]
    # ... do as many as needed, but you might not need so many ...

    return final_output

def make_part_of_output_1(input_grid) -> Tuple[np.ndarray, int]:
    # <comment describing what part of the output is being drawn>

    # returns (output, background_transparent)
    # output should be a grid of colors
    # background_transparent should indicate which color doesn't get copied into the final output

    return output, background_color

def make_part_of_output_2(input_grid) -> Tuple[np.ndarray, int]: # etc
```

Do the following:
1. Think step-by-step and brainstorm about what `main` is doing and how to break it up into a few smaller functions:
    (a) HINT: What are the different types of things that are being drawn to the output?
    (b) HINT: What are the different visual/image parts that are combined to make the output?
    (c) HINT: Use different subroutines to draw each kind of thing in the output
    (d) HINT: After your brainstorming, double check that you are following the directions and obeying the provided code template above. If not, try again.
2. Output code exactly following the above template in a Markdown Python block:
    (a) Each subroutine MUST ONLY take one argument, the original `input_grid` 
    (b) Each subroutine MUST ONLY return a pair of a color grid and a color indicating what is background/transparent
    (c) All subroutines MUST ONLY be combined like how they are in the template
    (d) Each subroutine should be called `make_part_of_output_1`, `make_part_of_output_2`