from common import *

import numpy as np
from typing import *

# concepts:
# patterns, translational symmetry, reflection, symmetry detection, positioning

# description:
# In the input, you will see a sprite repeated horizontally and vertically in a grid, and some of those repetitions might be reflected vertically.
# To make the output, just extract the repeated sprite in its non-reflected form.

def main(input_grid):
    # Find the period both horizontally and vertically
    for period in range(1, input_grid.shape[0]):
        # Extract the sprite and all of its repeated translated versions
        sprite = input_grid[:period, :period]
        repetitions = [
            input_grid[i*period:(i+1)*period, j*period:(j+1)*period]
            for i in range(input_grid.shape[0]//period)
            for j in range(input_grid.shape[1]//period)
        ]

        # Check that every repetition matches the sprite or its vertical reflection
        valid = True
        for rep in repetitions:
            reflections = [rep, np.flip(rep, 0)] # include vertical reflection
            if not any([np.array_equal(sprite, r) for r in reflections]):
                valid = False
                break

        if valid:
            return sprite

    assert False, "No valid period found"

def generate_input():
    # Create the sprite to be duplicated; pick a trio of random colors
    n = np.random.randint(2, 5)
    sprite = random_sprite(n, n, color_palette=np.random.choice(list(Color.NOT_BLACK), 3, replace=False).tolist())
    
    # Generate random reflections of the sprite and create a larger grid
    grid_size = 3 * n
    grid = np.zeros((grid_size, grid_size), dtype=int)

    for i in range(3):
        for j in range(3):
            if np.random.rand() > 0.5:
                reflected_sprite = np.flip(sprite, 0)
                blit_sprite(grid, reflected_sprite, x=i*n, y=j*n)
            else:
                blit_sprite(grid, sprite, x=i*n, y=j*n)

    return grid