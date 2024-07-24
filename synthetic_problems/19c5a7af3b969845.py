from common import *

import numpy as np
from typing import *

# concepts:
# collision detection, counting, horizontal/vertical bars

# description:
# In the input, you will see a grid with several 1x1 red pixels and one 2x2 blue square.
# First, count the number of red pixels and represent this value on the top row of the output grid as green pixels, one for each red pixel.
# Then, replace each red pixel in the input grid with a vertical bar.
# The output grid will show these vertical red bars along with the original blue square.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    red_pixel_locations = np.argwhere(input_grid == Color.RED)
    blue_square_locations = np.argwhere(input_grid == Color.BLUE)

    # Clear red pixels from the input grid for now
    output_grid[red_pixel_locations[:,0], red_pixel_locations[:,1]] = Color.BLACK
    
    # Count the number of red pixels
    red_pixel_count = len(red_pixel_locations)
    
    # Create the top row green representation for the count of red pixels
    green_representation = [Color.GREEN] * red_pixel_count
    output_grid[0, :red_pixel_count] = green_representation
    
    # Replace the red pixels with vertical bars
    for x, y in red_pixel_locations:
        output_grid[:, y] = Color.RED

    return output_grid

def generate_input() -> np.ndarray:
    # Create a random input grid between 8x8 to 15x15
    n = np.random.randint(8, 16)
    m = np.random.randint(8, 16)
    grid = np.full((n, m), Color.BLACK)

    # Place one 2x2 blue square randomly on the grid
    blue_square = np.full((2, 2), Color.BLUE)
    x, y = random_free_location_for_sprite(grid, blue_square, background=Color.BLACK, padding=1)
    blit_sprite(grid, blue_square, x, y, background=Color.BLACK)

    # Place a random number of red pixels (between 3 and 8) at random locations
    red_pixel = np.full((1,1), Color.RED)
    for _ in range(np.random.randint(3, 9)):
        x, y = random_free_location_for_sprite(grid, red_pixel, background=Color.BLACK)
        blit_sprite(grid, red_pixel, x, y, background=Color.BLACK)

    return grid