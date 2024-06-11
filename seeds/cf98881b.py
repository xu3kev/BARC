from common import *

import numpy as np
from typing import *

# concepts:
# patterns, copying, overlaying

# description:
# In the input, you will see a 4x14 grid divided into three 4x4 sections by orange vertical lines. 
# The sections display a yellow pattern, a maroon pattern, and a blue pattern from left to right.
# To make the output, you have to copy the blue pattern first, then overlay the maroon pattern over that, finally overlay the yellow pattern over that as well.

def main(input_grid):
    # get the blue pattern from the third section and copy it to make the base of the output grid
    blue_pattern = input_grid[10:14,0:4]
    output_grid = blue_pattern

    # get the maroon pattern from the second section and overlay it on output grid
    maroon_pattern = input_grid[5:9,0:4]
    output_grid = np.where(maroon_pattern, maroon_pattern, output_grid)

    # get the yellow pattern from the first section and overlay it on output grid
    yellow_pattern = input_grid[0:4,0:4]
    output_grid = np.where(yellow_pattern, yellow_pattern, output_grid)

    return output_grid

def generate_input():
    # make 4x14 black grid as background
    grid = np.zeros((14,4), dtype=int)

    # draw orange dividers to make three sections
    grid[4,:] = Color.ORANGE
    grid[9,:] = Color.ORANGE

    # scatter yellow pixels in first section
    for _ in range(12):
        x, y = random.randint(0, 3), random.randint(0, 3)
        grid[x, y] = Color.YELLOW

    # scatter maroon pixels in second section
    for _ in range(12):
        x, y = random.randint(5, 8), random.randint(0, 3)
        grid[x, y] = Color.MAROON
    
    # scatter blue pixels in third section
    for _ in range(12):
        x, y = random.randint(10, 13), random.randint(0, 3)
        grid[x, y] = Color.BLUE

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)