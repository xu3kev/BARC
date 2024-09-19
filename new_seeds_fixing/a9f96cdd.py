from common import *

import numpy as np
from typing import *

# concepts:
# pattern location

# description:
# In the input you will see one red pixel
# To make the output grid, you should 
# 1. draw a pattern with four different colors that centered at the red pixel
# 2. remove the red pixel

def main(input_grid):
    # Find out the position of the red pixel.
    red_x, red_y, w, h = bounding_box(grid=input_grid, background=Color.BLACK)

    # Get the specific surrounding pattern
    pattern = np.array([[Color.GREEN, Color.BLACK, Color.PINK], 
                        [Color.BLACK, Color.BLACK, Color.BLACK],
                        [Color.TEAL, Color.BLACK, Color.YELLOW]]).transpose()
    
    # Get the relative position of pattern on the output grid
    rela_x, rela_y = red_x - 1, red_y - 1

    # The output grid is the same size of input grid
    output_grid = np.copy(input_grid)
    output_grid = blit_sprite(grid=output_grid, x=rela_x, y=rela_y, sprite=pattern, background=Color.BLACK)

    # Remove the red pixel
    output_grid[red_x, red_y] = Color.BLACK

    return output_grid
    
def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 5, 3
    grid = np.zeros((n, m), dtype=int)

    # Randomly select the position of the red pixel and draw it.
    x, y = np.random.randint(0, n - 1), np.random.randint(0, m - 1)
    grid[x, y] = Color.RED
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)