from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, alignment, patterns

# description:
# In the input, you will see a grid with multiple identical shapes scattered around the grid. Each shape will have one pixel of a unique color.
# To make the output, align these shapes along the left side of the grid, maintaining their patterns and relative positions.
# The unique colored pixels will remain in their respective shapes.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Initialize an empty output grid
    output_grid = np.zeros_like(input_grid)

    # Find connected components ensuring they are monochromatic shapes with a unique color pixel
    shapes = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False, connectivity=4)

    # Sort shapes by their relative positions from top-left to bottom-right
    shapes_sorted = sorted(shapes, key=lambda obj: bounding_box(obj, background=Color.BLACK))

    # Align shapes along the left side, keeping their patterns
    y_offset = 0
    for shape in shapes_sorted:
        _, shape_y, shape_w, shape_h = bounding_box(shape, background=Color.BLACK)
        
        # Translate shape to the left side of the grid
        aligned_shape = translate(shape, x=0, y=-shape_y, background=Color.BLACK)
        
        # Ensure no overlap by stacking shapes vertically with some padding
        blit_sprite(output_grid, aligned_shape, x=0, y=y_offset)
        y_offset += shape_h + 1

    return output_grid

def generate_input() -> np.ndarray:
    # Define grid size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    input_grid = np.full((n, m), Color.BLACK, dtype=int)

    # Define number of shapes
    num_shapes = np.random.randint(2, 6)
    
    # Randomly generate shapes with unique colored pixels
    shape_size = np.random.randint(3, 5)
    shapes = []
    for _ in range(num_shapes):
        shape = random_sprite(shape_size, shape_size, density=0.5, color_palette=Color.NOT_BLACK)
        unique_color = np.random.choice(list(Color.NOT_BLACK))
        unique_pixel_pos = np.random.randint(0, shape_size, size=2)
        shape[unique_pixel_pos[0], unique_pixel_pos[1]] = unique_color
        shapes.append(shape)

    # Place the shapes randomly on the grid
    for shape in shapes:
        while True:
            try:
                x, y = random_free_location_for_sprite(input_grid, shape, padding=1, padding_connectivity=4)
                blit_sprite(input_grid, shape, x, y)
                break
            except:
                continue

    return input_grid