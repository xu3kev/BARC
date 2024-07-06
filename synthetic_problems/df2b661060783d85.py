from common import *

import numpy as np
from typing import *

# concepts:
# rotation, shape identification, pixel manipulation

# description:
# In the input, you will see several distinct shapes of arbitrary colors on a black background. Each shape should be rotated by 90 degrees clockwise in the output grid while retaining its position within the grid's bounding box.

def rotate_clockwise(shape):
    h, w = shape.shape
    new_shape = np.zeros((w, h), dtype=int)  # note the dimension swap
    for i in range(h):
        for j in range(w):
            new_shape[j, h - 1 - i] = shape[i, j]
    return new_shape

def main(input_grid):
    output_grid = np.zeros_like(input_grid)

    shapes = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False)

    for shape in shapes:
        x, y, w, h = bounding_box(shape)
        cropped_shape = shape[x:x+w, y:y+h]
        rotated_shape = rotate_clockwise(cropped_shape)
        for i in range(rotated_shape.shape[0]):
            for j in range(rotated_shape.shape[1]):
                if rotated_shape[i, j] != Color.BLACK:
                    output_grid[x+i, y+j] = rotated_shape[i, j]

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    for _ in range(np.random.randint(3, 7)):  # add a random number of shapes
        w, h = np.random.randint(2, 5), np.random.randint(2, 5)
        shape = random_sprite(w, h, color_palette=[np.random.choice(Color.NOT_BLACK)], connectivity=8)
        x, y = random_free_location_for_object(grid, shape)
        blit(grid, shape, x, y)

    return grid