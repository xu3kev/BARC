from common import *

import numpy as np
import random

# concepts:
# horizontal mirror symmetry
# occlusion

# description:
# In the input grid, you will see black and colored pixels forming various patterns. 
# To produce the output, you will reflect the grid horizontally over its mid-line, 
# ensuring that all the original patterns are maintained.

def main(input_grid):
    # Create output grid as a copy of input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Reflect the grid horizontally over its mid-line
    for x in range(height):
        for y in range(width // 2):
            output_grid[x, -(y + 1)] = input_grid[x, y]
    
    return output_grid


def generate_input():
    # Generate a grid of arbitrary size, between 6x6 and 20x20
    height = random.randint(6, 20)
    width = random.randint(6, 20)
    grid = np.zeros((height, width), dtype=int)
    
    # Generate random colored patterns on the grid
    num_patterns = random.randint(3, 10)
    for _ in range(num_patterns):
        w, h = random.randint(1, width // 2), random.randint(1, height)
        color = random.choice(list(Color.NOT_BLACK))
        x, y = random.randint(0, height - h), random.randint(0, width // 2 - w)
        sprite = random_sprite(h, w, density=0.5, color_palette=[color], connectivity=4)
        blit(grid, sprite, x, y)
        
    return grid