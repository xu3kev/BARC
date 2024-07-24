from common import *

import numpy as np
from typing import *

# concepts:
# patterns, objects, scaling, filling

# description:
# In the input, you will see a randomly sized 2x2 colored sprite located at a random position on a black grid.
# Scale this sprite to be 4x4 and fill it with the same color as the original sprite. Place the scaled sprite in the same relative position in the output grid.

def main(input_grid):
    # create the output grid with larger dimensions to accommodate the 4x4 scaled sprite
    n, m = input_grid.shape
    output_grid = np.zeros((n*2, m*2), dtype=int)

    # find the position of the 2x2 sprite
    for x in range(n-1):
        for y in range(m-1):
            colors = {input_grid[x, y], input_grid[x + 1, y], input_grid[x, y + 1], input_grid[x + 1, y + 1]}
            if len(colors) == 1 and list(colors)[0] != Color.BLACK:
                sprite_color = list(colors)[0]
                sprite_start_x, sprite_start_y = x, y
                break
    
    # draw a 4x4 scaled version of the sprite on the appropriate position in the output grid
    for dx in range(4):
        for dy in range(4):
            output_grid[sprite_start_x*2 + dx, sprite_start_y*2 + dy] = sprite_color
            
    return output_grid

def generate_input():
    # create a small grid (5x5) to ensure there's enough space for the sprite and randomness
    n, m = 5, 5
    grid = np.zeros((n, m), dtype=int)

    # create a 2x2 sprite with a random color at a random location within the grid
    sprite_color = np.random.choice(list(Color.NOT_BLACK))
    
    x = np.random.randint(0, n-1)
    y = np.random.randint(0, m-1)
    
    grid[x, y] = sprite_color
    grid[x+1, y] = sprite_color
    grid[x, y+1] = sprite_color
    grid[x+1, y+1] = sprite_color

    return grid