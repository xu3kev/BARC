from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with several color pixels on first row.
# To make the output, you should draw a chessboard pattern from each pixel.
# The chessboard pattern is expand one pixel to the left and right of the pixel, and expand down to the bottom of the grid.

def main(input_grid):
    # Extract the pixels
    pixels = find_connected_components(input_grid, monochromatic=True)
    pixels.sort(key=lambda x: object_position(x)[0])

    # Create output grid
    output_grid = np.zeros_like(input_grid)
    # Create the chessboard pattern for each pixel
    for pixel in pixels:
        x, y = object_position(pixel)
        pixel_color = object_colors(pixel)[0]
        for j in range(0, input_grid.shape[1], 2):
            # Color one pixel in each two pixels down the pixel's column
            output_grid[x, j] = pixel_color
            # Color the other one pixel in each two pixels down the pixel's left column
            if x - 1 >= 0 and j + 1 < input_grid.shape[1]:
                output_grid[x - 1, j + 1] = pixel_color
            # Color the other one pixel in each two pixels down the pixel's right column
            if x + 1 < input_grid.shape[0] and j + 1 < input_grid.shape[1]:
                output_grid[x + 1, j + 1] = pixel_color

    return output_grid
        

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose the number of pattern
    num_pattern = np.random.randint(1, 4)
    colors = np.random.choice(Color.NOT_BLACK, size=num_pattern, replace=False)

    # Randomly place one pixel on the top row of the grid, each two pixels has at least two pixels padding
    for i in range(num_pattern):
        first_row = np.array([grid[:, 0]]).T
        pixel = np.array([[1]])
        try:
            x, _ = random_free_location_for_sprite(grid=first_row, sprite=pixel, padding=2, padding_connectivity=4)
        except:
            # No more space for the pattern
            break
        grid[x, 0] = colors[i]
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
