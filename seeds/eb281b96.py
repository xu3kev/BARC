from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation, flipping

# description:
# In the input you will see a grid with wave patterns.
# To make the output, you should flip the input grid horizontally and place it in the output grid.
# And then place the flipped input grid in the output grid again.

def main(input_grid):
    # Create output grid
    input_n, input_m = input_grid.shape

    # The output grid is placing and flipping the original pattern 4 times
    n, m = input_n, (input_m - 1) * 4 + 1
    output_grid = np.zeros((n, m), dtype=int)

    # Flip the input grid horizontally
    flipped_input = np.fliplr(input_grid)

    # Place the input and flipped input in the output grid
    blit_sprite(output_grid, input_grid, x=0, y=0)
    blit_sprite(output_grid, flipped_input, x=0, y=input_m - 1)
    blit_sprite(output_grid, input_grid, x=0, y=2 * (input_m - 1))
    blit_sprite(output_grid, flipped_input, x=0, y=3 * (input_m - 1))

    return output_grid

def generate_input():
    # randomly select pattern number and pattern hight
    pattern_num = np.random.randint(3, 5)
    pattern_height = np.random.randint(3, 5)

    # Each pattern is 5 pixels wide
    n, m = pattern_num * 4 + 1, pattern_height
    grid = np.zeros((n, m), dtype=int)

    # Draw the pattern, which looks like a wave
    color = np.random.choice(Color.NOT_BLACK)
    for i in range(0, n, 4):
        grid[i, -1] = color
    for i in range(2, n, 4):
        grid[i, 0] = color
    for i in range(1, n, 2):
        draw_line(grid, x=i, y=1, end_x=i, end_y= m - 2, color=color, direction=(0, 1))
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
