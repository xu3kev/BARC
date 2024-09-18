from common import *

import numpy as np
from typing import *

# concepts:
# line drawing, obstacle recognition

# description:
# In the input you will see several red pixels on the bottom row of the grid, and some gray pixels scattered on the grid.
# To make the output grid, you should draw a red line from the bottom row to the top row. If it touch the gray pixel, 
# it should go right then up to avoid the gray pixel.

def main(input_grid):
    output_grid = input_grid.copy()
    for pos_x, item in enumerate(np.transpose(input_grid)[-1]):
        # Draw the red line from the bottom row to the top row.
        if item == Color.RED:
            for pos_y in reversed(range(10)):
                if output_grid[pos_x, pos_y] != Color.GRAY:
                    output_grid[pos_x, pos_y] = Color.RED
                else:
                    # If the red line touch the gray pixel, it should go right then up to avoid the gray pixel.
                    output_grid[pos_x + 1, pos_y + 1] = Color.RED
                    pos_x += 1
                    output_grid[pos_x, pos_y] = Color.RED
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # Generate the red pixels on the bottom row.
    available_postion = range(1, 9)
    red_location = random.sample(available_postion, 3)
    red_location.sort()

    # Ensure the red pixels are not too close to each other.
    while red_location[1] - red_location[0] < 2 or red_location[2] - red_location[1] < 2:
        red_location = random.sample(available_postion, 3)
        red_location.sort()
    
    # Generate the random gray pixels on the grid.
    num_gray = np.random.randint(2, 4)
    gray_locations = []
    for i in range(2):
        if i == 1:
            available_postion = range(1, 8)
        gray_location = random.sample(available_postion, num_gray)
        gray_location.sort()
        # Ensure the gray pixels are not too close to each other.
        while gray_location[1] - gray_location[0] < 2 or gray_location[-1] - gray_location[-2] < 2:
            gray_location = random.sample(available_postion, num_gray)
            gray_location.sort()
        gray_locations.append(gray_location)
    
    # Draw the red and gray pixels on the grid.
    for pos_x in red_location:
        grid[pos_x, -1] = Color.RED
    
    for pos_x, pos_y in zip(gray_locations[0], gray_locations[1]):
        grid[pos_x, pos_y] = Color.GRAY

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
