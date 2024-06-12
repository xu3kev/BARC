from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, growing

# description:
# In the input you will see individual pixels sprinkled on a black background that are either red, green, or blue
# Turn each red pixel into a vertical bar, and each green or blue pixel into a horizontal bar

def main(input_grid):

    # extract the pixels of each color
    red_pixels = (input_grid == Color.RED)
    green_pixels = (input_grid == Color.GREEN)
    blue_pixels = (input_grid == Color.BLUE)

    # prepare a blank output grid, because we don't need to reuse anything from the input (we're not drawing on top of the input)
    output_grid = np.zeros_like(input_grid)

    # turn red pixels into vertical bars
    red_locations = np.argwhere(red_pixels)
    for x, y in red_locations:
        # vertical means the same X value
        output_grid[x, :] = Color.RED
    
    # turn green and blue pixels into horizontal bars
    green_locations = np.argwhere(green_pixels)
    blue_locations = np.argwhere(blue_pixels)
    for x, y in green_locations:
        # horizontal means the same Y value
        output_grid[:, y] = Color.GREEN
    for x, y in blue_locations:
        # horizontal means the same Y value
        output_grid[:, y] = Color.BLUE
    
    return output_grid



def generate_input():
    # make a black grid, of a random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # sprinkle some red, green, and blue pixels
    num_red, num_green, num_blue = np.random.randint(1, 5), np.random.randint(1, 5), np.random.randint(1, 5)
    for _ in range(num_red):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED
    for _ in range(num_green):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.GREEN
    for _ in range(num_blue):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.BLUE

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)