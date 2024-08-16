from common import *

import numpy as np
from typing import *

# description:
# To create the output grid, generate and place all 8 symmetries (4 rotations and 4 flips) of the object around the original object.
# Ensure that each symmetrical version of the object appears exactly once.

def main(input_grid):
    # Find the single object in the input grid
    objects = find_connected_components(input_grid, monochromatic=False, background=Color.BLACK)
    assert len(objects) == 1, "Expected exactly one object in the input grid"

    obj = objects[0]
    sprite = crop(obj)

    # Generate all 8 symmetrical versions of the object (4 rotations and 4 flips)
    sprite_variations = [
        sprite,
        np.rot90(sprite),
        np.rot90(sprite, 2),
        np.rot90(sprite, 3),
        np.flipud(sprite),
        np.fliplr(sprite),
        np.flipud(np.rot90(sprite)),
        np.fliplr(np.rot90(sprite))
    ]

    # Create a larger output grid to fit all variations around the original
    obj_height, obj_width = sprite.shape[:2]
    grid_height = grid_width = 3 * max(obj_height, obj_width)
    output_grid = np.full((grid_height, grid_width), Color.BLACK)

    # Calculate the center of the output grid
    center_y, center_x = grid_height // 2, grid_width // 2

    # Place the original object at the center
    blit_sprite(output_grid, sprite, center_y - obj_height // 2, center_x - obj_width // 2)

    # Define positions around the center to place symmetrical variations
    positions = [
        (center_y - obj_height, center_x - obj_width),
        (center_y - obj_height, center_x),
        (center_y - obj_height, center_x + obj_width),
        (center_y, center_x - obj_width),
        (center_y, center_x + obj_width),
        (center_y + obj_height, center_x - obj_width),
        (center_y + obj_height, center_x),
        (center_y + obj_height, center_x + obj_width)
    ]

    for pos, var_sprite in zip(positions, sprite_variations):
        blit_sprite(output_grid, var_sprite, pos[0], pos[1])

    return output_grid


def generate_input():
    # Create a random sized grid for the input
    n, m = np.random.randint(8, 12), np.random.randint(8, 12)
    grid = np.full((n, m), Color.BLACK)

    # Generate a random multicolored object
    proto_obj = random_sprite(np.random.randint(3, 5), np.random.randint(3, 5), density=0.5, color_palette=Color.NOT_BLACK)

    # Place the object randomly on the grid
    x, y = random_free_location_for_sprite(grid, proto_obj, padding=1, border_size=1, background=Color.BLACK)
    blit_sprite(grid, proto_obj, x, y)

    return grid