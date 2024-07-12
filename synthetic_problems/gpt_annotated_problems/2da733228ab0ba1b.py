from common import *

import numpy as np
from typing import *

# concepts:
# objects, flood fill, connectivity, scaling, colors as indicators

# description:
# In the input, you will see a black grid with a blue line that starts in the top left corner and moves in a random walk until it reaches the bottom of the grid.
# To make the output:
# 1. Find the black regions separated by the blue line.
# 2. For each region, count the number of pixels it contains.
# 3. Create a new grid that is twice the size of the input grid in both dimensions.
# 4. For each region in the input:
#    - If the region's size is prime, fill the corresponding region in the output with red.
#    - If the region's size is even, fill the corresponding region in the output with green.
#    - If the region's size is odd but not prime, fill the corresponding region in the output with yellow.
# 5. Copy the blue line from the input to the output, scaling it up by a factor of 2.

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main(input_grid):
    # Create output grid
    output_grid = np.zeros((input_grid.shape[0]*2, input_grid.shape[1]*2), dtype=int)

    # Find black regions
    black_regions = find_connected_components(input_grid, connectivity=4, background=Color.BLUE)

    # Process each region
    for region in black_regions:
        size = np.sum(region == Color.BLACK)
        color = Color.YELLOW  # Default color for odd non-prime numbers
        if is_prime(size):
            color = Color.RED
        elif size % 2 == 0:
            color = Color.GREEN

        # Find the bounding box of the region
        x, y, w, h = bounding_box(region, background=Color.BLUE)

        # Fill the corresponding region in the output grid
        for i in range(x*2, (x+w)*2):
            for j in range(y*2, (y+h)*2):
                if region[i//2-x, j//2-y] == Color.BLACK:
                    output_grid[i, j] = color

    # Copy and scale up the blue line
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == Color.BLUE:
                output_grid[i*2, j*2] = Color.BLUE
                output_grid[i*2+1, j*2] = Color.BLUE
                output_grid[i*2, j*2+1] = Color.BLUE
                output_grid[i*2+1, j*2+1] = Color.BLUE

    return output_grid

def generate_input():
    # Make a black grid that is between 10 and 20 cells wide and tall
    width = np.random.randint(10, 21)
    height = np.random.randint(10, 21)
    grid = np.zeros((width, height), dtype=int)

    # Make a blue line that starts in the top left corner and moves in a random walk until it reaches the bottom
    x, y = 0, 0
    while y < height - 1:
        grid[x, y] = Color.BLUE
        dx = np.random.choice([-1, 0, 1])
        if x + dx < 0 or x + dx >= width:
            dx = 0
        x += dx
        y += 1

    # Fill the last row
    grid[x, y] = Color.BLUE

    return grid