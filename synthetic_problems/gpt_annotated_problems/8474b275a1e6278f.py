from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, sliding objects, occlusion

# description:
# In the input grid, you will see a symmetric U-shaped object of one color in a black grid, with pixels of another color scattered around the grid.
# To produce the output grid:
# 1. Slide the U-shaped object down by one pixel.
# 2. For each colored pixel that is now inside the U-shape, extend it vertically in both directions until it reaches the boundary of the U or the edge of the grid.
# 3. If any extended line reaches the top of the U, it should continue through the U, effectively cutting it.

def main(input_grid):
    # Find the U-shaped object
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    u_shape = max(objects, key=lambda o: np.count_nonzero(o))

    # Get the color of the U-shape
    u_color = u_shape[u_shape != Color.BLACK][0]

    # Get the color of the scattered pixels
    colors = np.unique(input_grid)
    pixel_color = [c for c in colors if c not in [Color.BLACK, u_color]][0]

    # Create output grid and slide U-shape down by one pixel
    output_grid = np.full_like(input_grid, Color.BLACK)
    output_grid[1:, :] = u_shape[:-1, :]

    # Process each colored pixel
    for x in range(input_grid.shape[1]):
        for y in range(input_grid.shape[0]):
            if input_grid[y, x] == pixel_color:
                # Check if the pixel is now inside the U-shape
                if output_grid[y, x] == Color.BLACK:
                    # Extend upwards
                    for up_y in range(y, -1, -1):
                        if output_grid[up_y, x] == u_color:
                            # Cut through the U
                            output_grid[up_y, x] = pixel_color
                        elif output_grid[up_y, x] == Color.BLACK:
                            output_grid[up_y, x] = pixel_color
                        else:
                            break
                    
                    # Extend downwards
                    for down_y in range(y, output_grid.shape[0]):
                        if output_grid[down_y, x] == Color.BLACK:
                            output_grid[down_y, x] = pixel_color
                        else:
                            break

    return output_grid

def generate_input():
    # Create a 20x20 black grid
    input_grid = np.full((20, 20), Color.BLACK)

    # Choose colors for U-shape and pixels
    u_color, pixel_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # Create the U-shape
    u_shape = np.full((8, 6), Color.BLACK)
    u_shape[0, :] = u_color  # Top
    u_shape[:, 0] = u_color  # Left side
    u_shape[:, -1] = u_color  # Right side

    # Ensure symmetry
    u_shape = np.maximum(u_shape, np.fliplr(u_shape))

    # Place U-shape in the upper half of the grid
    x, y = np.random.randint(0, 20 - 6), np.random.randint(0, 10 - 8)
    blit_sprite(input_grid, u_shape, x=x, y=y)

    # Generate 5-25 pixels at random unfilled spots
    n_pixels = np.random.randint(5, 26)
    x_choices, y_choices = np.where(input_grid == Color.BLACK)
    location_choices = list(zip(x_choices, y_choices))
    pixel_locations = random.sample(location_choices, n_pixels)
    for x, y in pixel_locations:
        input_grid[y, x] = pixel_color

    return input_grid