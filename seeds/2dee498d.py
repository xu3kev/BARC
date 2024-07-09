from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, reflection

# description:
# In the input, you will see a sprite repeated horizontally, and some of those repetitions might be reflected top/down/right/left.
# To make the output, just extract the repeated sprite.

def main(input_grid):
    # Find the period, remembering that we need to consider reflections
    for period in range(1, input_grid.shape[0]):
        # Extract the sprite and all of its repeated translated versions
        sprite = input_grid[:period]
        repetitions = [ input_grid[i*period:(i+1)*period] for i in range(input_grid.shape[0]//period) ]

        # Check that every repetition matches the sprite, or a reflection of the sprite
        valid = True
        for rep in repetitions:
            reflections = [rep, np.flip(rep, 0), np.flip(rep, 1)]
            if not any([np.array_equal(sprite, r) for r in reflections]):
                valid = False

        if valid:
            return sprite
        
    assert False, "No valid period found"

def generate_input():
    # Create the sprite to be duplicated; pick a trio of random colors
    n = random.randint(2,7)
    sprite = random_sprite(n, n, color_palette=random.sample(list(Color.NOT_BLACK),3))
    
    # Duplicate the sprite 3 times horizontally
    grid = np.zeros((3*n, n),dtype=int)
    for i in range(3):
        blit_sprite(grid, sprite, x=i*n, y=0)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)