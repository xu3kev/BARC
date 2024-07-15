from common import *

import numpy as np
from typing import *

# concepts:
# growing, alignment, vertical lines, horizontal lines

# description:
# In the input you will see individual pixels sprinkled on a black background that are either red, green, blue, yellow, or orange.
# Turn each red pixel into a vertical bar extending upwards, each green pixel into a vertical bar extending downwards,
# blue pixels into horizontal bars extending to the left, yellow pixels into horizontal bars extending to the right,
# and orange pixels into both vertical and horizontal bars (like a cross).

def main(input_grid):
    # extract the pixels of each color
    red_pixels = (input_grid == Color.RED)
    green_pixels = (input_grid == Color.GREEN)
    blue_pixels = (input_grid == Color.BLUE)
    yellow_pixels = (input_grid == Color.YELLOW)
    orange_pixels = (input_grid == Color.ORANGE)
    
    # prepare a blank output grid
    output_grid = np.zeros_like(input_grid, dtype=int)

    # grow red pixels into vertical bars extending upwards
    red_locations = np.argwhere(red_pixels)
    for x, y in red_locations:
        output_grid[:x+1, y] = Color.RED
    
    # grow green pixels into vertical bars extending downwards
    green_locations = np.argwhere(green_pixels)
    for x, y in green_locations:
        output_grid[x:, y] = Color.GREEN
    
    # grow blue pixels into horizontal bars extending to the left
    blue_locations = np.argwhere(blue_pixels)
    for x, y in blue_locations:
        output_grid[x, :y+1] = Color.BLUE

    # grow yellow pixels into horizontal bars extending to the right
    yellow_locations = np.argwhere(yellow_pixels)
    for x, y in yellow_locations:
        output_grid[x, y:] = Color.YELLOW

    # grow orange pixels into both vertical and horizontal bars (like a cross)
    orange_locations = np.argwhere(orange_pixels)
    for x, y in orange_locations:
        output_grid[:x+1, y] = Color.ORANGE
        output_grid[x:, y] = Color.ORANGE
        output_grid[x, :y+1] = Color.ORANGE
        output_grid[x, y:] = Color.ORANGE

    return output_grid

def generate_input():
    # make a black grid, of a random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # sprinkle some red, green, blue, yellow, and orange pixels
    num_red, num_green, num_blue, num_yellow, num_orange = (np.random.randint(1, 5) for _ in range(5))
    
    for _ in range(num_red):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED
    for _ in range(num_green):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.GREEN
    for _ in range(num_blue):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.BLUE
    for _ in range(num_yellow):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.YELLOW
    for _ in range(num_orange):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.ORANGE

    return grid