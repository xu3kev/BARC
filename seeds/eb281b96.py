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
    # Plan:
    # 1. Create output grid
    # 2. Flip the input grid horizontally and put it in the output repeatedly

    # 1. Create output grid
    input_width, input_height = input_grid.shape
    # The output grid is placing and flipping the original pattern 4 times
    output_width, output_height = input_width, (input_height - 1) * 4 + 1
    output_grid = np.full((output_width, output_height), Color.BLACK)

    # 2. Make the output by flipping the input and ultimately putting 4 copies (some flipped) into the output
    # Flip the input grid horizontally
    flipped_input = np.fliplr(input_grid)

    # Place the input and flipped input in the output grid
    blit_sprite(output_grid, input_grid, x=0, y=0)
    blit_sprite(output_grid, flipped_input, x=0, y=input_height - 1)
    blit_sprite(output_grid, input_grid, x=0, y=2 * (input_height - 1))
    blit_sprite(output_grid, flipped_input, x=0, y=3 * (input_height - 1))

    return output_grid

def generate_input():
    # randomly select pattern number and pattern hight
    pattern_num = np.random.randint(3, 5)
    pattern_height = np.random.randint(3, 5)

    # Each pattern is 5 pixels wide
    width, height = pattern_num * 4 + 1, pattern_height
    grid = np.full((width, height), Color.BLACK)

    # Draw the pattern, which looks like a wave
    color = np.random.choice(Color.NOT_BLACK)
    for x in range(0, width, 4):
        grid[x, -1] = color
    for x in range(2, width, 4):
        grid[x, 0] = color
    for x in range(1, width, 2):
        draw_line(grid, x=x, y=1, end_x=x, end_y=height-2, color=color, direction=(0, 1))
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
