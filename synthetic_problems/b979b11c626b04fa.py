from common import *

import numpy as np
from typing import *

# concepts:
# patterns, symmetry, mirroring, reflection, color

# description:
# In the input, you will see a random colorful pattern that may have a vertical or horizontal symmetry axis.
# To make the output, identify whether the pattern has vertical or horizontal symmetry. 
# Mirror the pattern along its symmetry axis to create a complete symmetric figure.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    
    # Check for vertical symmetry
    is_vertically_symmetric = np.all(input_grid == input_grid[:, ::-1])

    # Check for horizontal symmetry
    is_horizontally_symmetric = np.all(input_grid == input_grid[::-1, :])

    # Mirror according to the found symmetry or return the original if no symmetry
    if is_vertically_symmetric:
        mirrored_grid = np.concatenate((input_grid, input_grid[:, ::-1]), axis=1)
    elif is_horizontally_symmetric:
        mirrored_grid = np.concatenate((input_grid, input_grid[::-1, :]), axis=0)
    else:
        mirrored_grid = np.copy(input_grid)

    return mirrored_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(3, 7, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Decide on the type of symmetry: vertical, horizontal, or none
    symmetry_type = np.random.choice(["vertical", "horizontal", "none"])

    if symmetry_type == "vertical":
        half_grid = np.random.choice(Color.NOT_BLACK, size=(n, m // 2))
        grid[:, :m // 2] = half_grid
        grid[:, m // 2:] = half_grid[:, ::-1]
    elif symmetry_type == "horizontal":
        half_grid = np.random.choice(Color.NOT_BLACK, size=(n // 2, m))
        grid[:n // 2] = half_grid
        grid[n // 2:] = half_grid[::-1, :]
    else:
        grid = np.random.choice(Color.NOT_BLACK, size=(n, m))

    return grid