from common import *

import numpy as np
from typing import *

# concepts:
# grow, patterns, objects

# description:
# In the input, you will see a set of shapes of different colors, placed randomly on a grid with a black background.
# For each shape, extend it vertically and horizontally to form a grid of equally sized, non-overlapping cells, colored as the shape's original color.
# The output should preserve the horizontal and vertical rows of the input without any overlapping cells, ensuring no shape extends beyond the other shapes.

def main(input_grid):
    # find the unique color shapes (connected components) excluding the background
    background_color = Color.BLACK
    shapes = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=True)

    # create an output grid initialized to the background color
    output_grid = input_grid.copy()

    for shape in shapes:
        shape_color = shape[shape != background_color][0]
        x_min, y_min, width, height = bounding_box(shape, background=background_color)
        
        for x in range(x_min, x_min + width):
            for y in range(y_min, y_min + height):
                if input_grid[x, y] == shape_color:
                    # extend horizontally
                    output_grid[x, y_min:y_min+height] = shape_color
                    # extend vertically
                    output_grid[x_min:x_min+width, y] = shape_color

    return output_grid

def generate_input():
    grid_size = np.random.randint(10, 21)  # random size between 10 and 20
    grid = np.full((grid_size, grid_size), Color.BLACK)

    num_shapes = np.random.randint(2, 5)  # place between 2 to 4 shapes

    for _ in range(num_shapes):
        # Generate a random shape (1x1 to 3x3)
        shape_size = np.random.randint(1, 4)
        shape = random_sprite(shape_size, shape_size)
        shape_color = random.choice(list(Color.NOT_BLACK))

        # Fill the shape with the same color
        shape[shape != Color.BLACK] = shape_color

        x, y = random_free_location_for_sprite(grid, shape, background=Color.BLACK, padding=1)
        blit_sprite(grid, shape, x, y)
    
    return grid