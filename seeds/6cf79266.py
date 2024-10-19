from common import *

import numpy as np
from typing import *

# concepts:
# rectangle detection, background shape detection

# description:
# In the input you will see a grid with scattered one color pixels
# To make the output grid, you should detect the 3x3 black square in the random color pattern
# and replace it with a 3x3 blue square

def main(input_grid):
    # Plan: 
    # 1. Detect the 3x3 regions that are all black
    # 2. Draw a blue 3x3 in those regions

    # 1. Detect the 3x3 regions that are all black
    region_len = 3
    output_grid = np.copy(input_grid)
    matching_regions = [(x, y) for x in range(len(input_grid) - (region_len - 1)) for y in range(len(input_grid[0]) - (region_len - 1)) if np.all(input_grid[x:x + region_len, y:y + region_len] == Color.BLACK)]

    # 2. Draw a blue 3x3 in those regions
    for x, y in matching_regions:
        # Check if the region is all black
        if np.all(output_grid[x:x+region_len, y:y+region_len] == Color.BLACK):
            output_grid[x:x+region_len, y:y+region_len] = Color.BLUE

    return output_grid    

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 20, 20
    grid = np.zeros((n, m), dtype=int)

    # Get the random scatter color pixels on the grid.
    avaliable_colors = [c for c in Color.NOT_BLACK if c != Color.BLUE]
    background_color = np.random.choice(avaliable_colors)
    
    # Generate random color pixels on the grid.
    randomly_scatter_points(grid, color=background_color, density=0.7)

    # Randomly generate the number of black squares.
    square_num = np.random.randint(1, 4)

    # Generate the black squares on the grid.
    square_len = 3
    for _ in range(square_num):
        square = np.full((square_len, square_len), Color.BLACK)
        try:
            # Get the random free location for the black square.
            x, y = random_free_location_for_sprite(grid=grid, sprite=square, background=background_color)
        except:
            continue
        # Blit the black square on the grid.
        grid = blit_sprite(grid=grid, sprite=square, x=x, y=y, background=background_color)
     
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
