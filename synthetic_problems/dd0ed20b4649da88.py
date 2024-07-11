from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, patterns, surrounding

# description:
# In the input grid, you will see a T-shaped object of one color in a black grid, with pixels of another color scattered around the grid.
# To produce the output grid, for each colored pixel not part of the T-shape:
# 1. If it's directly below the T-shape, extend it upwards until it touches the T.
# 2. If it's not below the T-shape, surround it with a 3x3 square of its color (without overwriting the T-shape).
# The T-shape itself should remain unchanged in the output.

def main(input_grid):
    # Find the T-shape (largest connected component)
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    t_shape = max(objects, key=lambda o: np.count_nonzero(o))

    # Get the color of the T-shape
    t_color = t_shape[t_shape != Color.BLACK][0]

    # Get the color of the scattered pixels
    colors = np.unique(input_grid)
    pixel_color = [c for c in colors if c not in [Color.BLACK, t_color]][0]

    output_grid = input_grid.copy()

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] == pixel_color:
                # Check if the pixel is directly below the T-shape
                above_pixel = False
                for dy in range(y-1, -1, -1):
                    if input_grid[x, dy] == t_color:
                        above_pixel = True
                        break
                
                if above_pixel:
                    # Extend upwards until touching the T
                    output_grid[x, dy+1:y+1] = pixel_color
                else:
                    # Surround with a 3x3 square
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]:
                                if input_grid[nx, ny] != t_color:
                                    output_grid[nx, ny] = pixel_color

    return output_grid

def generate_input():
    # Create a 20x20 black grid
    input_grid = np.full((20, 20), Color.BLACK)

    # Choose a T-shape color and pixel color
    t_color, pixel_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # Create the T-shape
    t_shape = np.full((5, 5), Color.BLACK)
    t_shape[0, 1:4] = t_color
    t_shape[1:5, 2] = t_color

    # Put the T-shape at a random location in the upper half of the grid
    x, y = np.random.randint(0, 15), np.random.randint(0, 10)
    blit_sprite(input_grid, t_shape, x=x, y=y)

    # Generate 5-25 pixels at random (unfilled) spots
    n_pixels = np.random.randint(5, 26)
    x_choices, y_choices = np.where(input_grid == Color.BLACK)
    location_choices = list(zip(x_choices, y_choices))
    pixel_locations = random.sample(location_choices, n_pixels)
    for x, y in pixel_locations:
        input_grid[x, y] = pixel_color

    return input_grid