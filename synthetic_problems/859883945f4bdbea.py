from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, growing, color

# description:
# In the input you will see individual pixels sprinkled on a black background that are either red, green, or blue
# Turn each red pixel into a vertical bar starting from the top going downwards, each green pixel into a horizontal bar starting from the left going to the right, and each blue pixel into a square bar expanding equally in all directions.

def main(input_grid):

    # extract the pixels of each color
    red_pixels = (input_grid == Color.RED)
    green_pixels = (input_grid == Color.GREEN)
    blue_pixels = (input_grid == Color.BLUE)

    # prepare an output grid
    output_grid = np.copy(input_grid)

    # turn red pixels into vertical bars growing downward
    red_locations = np.argwhere(red_pixels)
    for x, y in red_locations:
        output_grid[x:, y] = Color.RED

    # turn green pixels into horizontal bars growing rightward
    green_locations = np.argwhere(green_pixels)
    for x, y in green_locations:
        output_grid[x, y:] = Color.GREEN

    # turn blue pixels into squares expanding equally in all directions
    blue_locations = np.argwhere(blue_pixels)
    for x, y in blue_locations:
        size = 0
        while True:
            min_x = max(x - size, 0)
            max_x = min(x + size + 1, output_grid.shape[0])
            min_y = max(y - size, 0)
            max_y = min(y + size + 1, output_grid.shape[1])
            
            if min_x == 0 and max_x == output_grid.shape[0] and min_y == 0 and max_y == output_grid.shape[1]:
                break

            output_grid[min_x:max_x, min_y:max_y] = Color.BLUE
            size += 1
    
    return output_grid

def generate_input():
    # create a grid of a random size between 10x10 and 19x19 filled with black
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)

    # sprinkle red, green, and blue pixels
    num_red = np.random.randint(1, 5)
    num_green = np.random.randint(1, 5)
    num_blue = np.random.randint(1, 5)
    
    for _ in range(num_red):
        x, y = np.random.randint(n), np.random.randint(m)
        grid[x, y] = Color.RED
        
    for _ in range(num_green):
        x, y = np.random.randint(n), np.random.randint(m)
        grid[x, y] = Color.GREEN

    for _ in range(num_blue):
        x, y = np.random.randint(n), np.random.randint(m)
        grid[x, y] = Color.BLUE

    return grid