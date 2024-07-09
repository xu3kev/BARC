from common import *

import numpy as np
from typing import *

# concepts:
# borders, pixel manipulation, counting

# description:
# In the input you will see a grid with various colored shapes on a black background.
# To make the output:
# 1. Draw a border around the entire grid with a thickness of one pixel. The border should be teal.
# 2. For each non-black shape in the input:
#    a. Count the number of pixels in the shape.
#    b. If the count is even, fill the shape with red.
#    c. If the count is odd, fill the shape with blue.
# 3. The black background should remain black.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Draw the teal border
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(1,0))
    draw_line(grid=output_grid, x=n-1, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=m-1, length=None, color=Color.TEAL, direction=(1,0))

    # Find and process each shape
    shapes = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    for shape in shapes:
        pixel_count = np.sum(shape != Color.BLACK)
        fill_color = Color.RED if pixel_count % 2 == 0 else Color.BLUE
        shape[shape != Color.BLACK] = fill_color
        blit_object(output_grid, shape, background=Color.BLACK)

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Generate 3-5 random shapes
    num_shapes = np.random.randint(3, 6)
    colors = random.sample(list(Color.NOT_BLACK), num_shapes)

    for color in colors:
        shape_size = np.random.randint(3, 7)
        shape = np.full((shape_size, shape_size), color)
        
        # Randomly remove some pixels to create irregular shapes
        mask = np.random.random(shape.shape) > 0.3
        shape[~mask] = Color.BLACK

        x, y = random_free_location_for_sprite(grid, shape, background=Color.BLACK, padding=1)
        blit_sprite(grid, shape, x, y)

    return grid