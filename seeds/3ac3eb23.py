from common import *

import numpy as np
from typing import *

# concepts:
# pixel pattern generation, falling downward

# description:
# In the input you will see a grid with several colored pixels at the top.
# To make the output, you should draw a pattern downward from each pixel:
# Color the diagonal corners, and then color downward with a vertical period of 2 from those corners and from the original pixel, making the pattern fall downward.

def main(input_grid):
    # Plan:
    # 1. Find the pixels and make the output
    # 2. Grow the pixel pattern downward from each pixel

    # Extract the pixels
    pixels = find_connected_components(input_grid, monochromatic=True, background=Color.BLACK)

    # Create output grid
    output_grid = np.full_like(input_grid, Color.BLACK)
    width, height = input_grid.shape

    # 2. Grow the pixel pattern downward from each pixel
    for pixel in pixels:
        pixel_x, pixel_y = object_position(pixel, background=Color.BLACK)
        pixel_color = object_colors(pixel)[0]

        # We do the diagonal corners *and* also the original pixel, so one of the offsets is 0,0
        for offset_x, offset_y in [(0, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            x, y = offset_x + pixel_x, offset_y + pixel_y

            # Fall downward (w/ period 2)
            while 0 <= x < width and 0 <= y < height:
                output_grid[x, y] = pixel_color
                # Vertical period of 2
                y += 2
            
    return output_grid


def generate_input():
    # Generate the background grid
    width, height = np.random.randint(10, 20, size=2)
    grid = np.zeros((width, height), dtype=int)

    # Randomly choose the number of pattern
    num_pixels = np.random.randint(1, 4)
    colors = np.random.choice(Color.NOT_BLACK, size=num_pixels, replace=False)

    # Randomly place one pixel on the top row of the grid, each two pixels has at least two pixels padding
    for i in range(num_pixels):
        pixel_sprite = np.full((1,1), colors[i])
        # Find a free spot but just in the top row
        top_y = 0
        top_row = grid[:, top_y:top_y+1]        
        try:
            x, _ = random_free_location_for_sprite(top_row, pixel_sprite, padding=2, padding_connectivity=4)
        except:
            # No more space
            break
        blit_sprite(grid, pixel_sprite, x, top_y)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
