from common import *

import numpy as np
from typing import *

# concepts:
# objects, scaling, collision detection, color guide

# description:
# In the input, you will see two objects: a large multicolored complex shape and a smaller simple monochromatic shape.
# To create the output, scale up the smaller shape proportionally to the size difference between the input grid and the smaller shape.
# Then translate the scaled shape on the grid until it touches the large multicolored shape.
# Once contact is made, zero out the touching region of the multicolored shape using the same dimensions as the smaller shape.

def main(input_grid: np.ndarray) -> np.ndarray:
    # find the connected components
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # separate out the smaller monochromatic shape and the large multicolored shape
    small_shape = large_shape = None
    for obj in objects:
        if len(set(obj.flatten())) == 2:  # one color + background
            small_shape = obj
        else:
            large_shape = obj

    assert small_shape is not None and large_shape is not None

    # compute the scaling factor based on grid differences
    small_x, small_y, small_w, small_h = bounding_box(small_shape)
    large_x, large_y, large_w, large_h = bounding_box(large_shape)

    scale_factor = min(large_w // small_w, large_h // small_h)
    scaled_shape = np.kron(small_shape[small_x:small_x+small_w, small_y:small_y+small_h], np.ones((scale_factor, scale_factor), dtype=int))

    # translate the scaled shape until it touches the large shape
    output_grid = input_grid.copy()
    found_contact = False

    for x in range(output_grid.shape[0] - scaled_shape.shape[0] + 1):
        for y in range(output_grid.shape[1] - scaled_shape.shape[1] + 1):
            translated_shape = translate(small_shape, x - small_x, y - small_y)
            if contact(object1=large_shape, object2=translated_shape):
                # zero out the overlapping region
                x_start, y_start = x, y
                x_end, y_end = x + scaled_shape.shape[0], y + scaled_shape.shape[1]
                
                for i in range(scaled_shape.shape[0]):
                    for j in range(scaled_shape.shape[1]):
                        if translated_shape[i, j] != Color.BLACK:
                            output_grid[x_start + i, y_start + j] = Color.BLACK

                found_contact = True
                break
        if found_contact:
            break

    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(15, 20), np.random.randint(15, 20)
    grid = np.full((n, m), Color.BLACK)

    # determine size and position of the multicolored large shape
    lw, lh = np.random.randint(8, n - 2), np.random.randint(8, m - 2)
    large_shape = random_sprite(lw, lh, density=0.7, symmetry=None, color_palette=Color.NOT_BLACK)

    # determine size and position of the small monochromatic shape
    sw, sh = np.random.randint(2, 6), np.random.randint(2, 6)
    color = np.random.choice(list(Color.NOT_BLACK))
    small_shape = random_sprite(sw, sh, density=0.7, symmetry=None, color_palette=[color])

    # place the large shape randomly in the grid
    x, y = random_free_location_for_sprite(grid, large_shape, border_size=0, padding=0, background=Color.BLACK)
    blit_sprite(grid, large_shape, x, y)

    # place the small shape randomly in the grid without touching the large shape
    x2, y2 = random_free_location_for_sprite(grid, small_shape, border_size=0, padding=0, background=Color.BLACK)
    while contact(object1=large_shape, object2=small_shape, x2=x2 - x, y2=y2 - y):
        x2, y2 = random_free_location_for_sprite(grid, small_shape, border_size=0, padding=0, background=Color.BLACK)
    blit_sprite(grid, small_shape, x2, y2)

    return grid