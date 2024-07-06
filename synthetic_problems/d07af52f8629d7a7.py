from common import *

import numpy as np
from typing import *

# concepts:
# connected components labeling, pattern repetition

# description:
# In the input, you will see several different shapes (connected components) of arbitrary colors scattered across the grid.
# Each shape can be uniquely identified. The task is to count how many shapes of each unique size are present.
# Then, repeat each unique shape in a new grid where the number of repetitions equals the number of shapes of that size.

def main(input_grid):
    # Find the connected components (shapes) in the grid
    shapes = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # Dictionary to store shape size and their counts
    shape_count = {}
    repeated_shapes = {}

    # Count unique shapes by size and store the first occurrence for repetition
    for shape in shapes:
        h, w = shape.shape
        size = (h, w)
        if size not in shape_count:
            shape_count[size] = 0
            repeated_shapes[size] = shape
        shape_count[size] += 1

    # Create the output_grid based on the largest shape size
    max_h = max(size[0] for size in shape_count.keys())
    max_w = max(size[1] for size in shape_count.keys())
    total_repetitions = sum(shape_count.values())
    output_grid_height = max_h * total_repetitions + total_repetitions - 1
    output_grid_width = max_w * total_repetitions + total_repetitions - 1
    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)
    
    # Place the repeated shapes in the output grid
    current_y = 0
    for size, count in shape_count.items():
        shape = repeated_shapes[size]
        for _ in range(count):
            current_x = 0
            blit(output_grid, shape, x=current_x, y=current_y, background=Color.BLACK)
            current_x += max_w + 1
        current_y += max_h + 1

    return output_grid


def generate_input():
    # make a black grid of random size between 10x10 to 20x20
    n, m = np.random.randint(10, 20, 2)
    grid = np.zeros((n,m), dtype=int)

    # randomly generate objects onto the grid
    num_objects = np.random.randint(3, 7)
    for _ in range(num_objects):
        color = np.random.choice(Color.NOT_BLACK)
        height = np.random.randint(1, n // 2)
        width = np.random.randint(1, m // 2)
        shape = random_sprite(height, width, color_palette=[color], connectivity=8)
        x, y = random_free_location_for_object(grid, shape, border_size=1)
        blit(grid, shape, x, y)

    return grid