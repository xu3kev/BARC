from common import *

import numpy as np
from typing import *

# concepts:
# objects, topology, puzzle piece, holes, rotation

# description:
# In the input, you will see multiple blue rectangular objects, each with a uniquely shaped black hole inside of it. There are also red objects somewhere that are exactly the same shape as each hole, but they may be rotated. 
# To make the output, check if each red object can fit perfectly inside a black hole of a blue object when rotated 0, 90, 180, or 270 degrees. If it does, place it inside the black hole in the correct orientation. If it doesn't fit anywhere, leave it where it is.

def main(input_grid):
    # Parse the input into blue objects and red objects
    blue_input = input_grid.copy()
    blue_input[input_grid != Color.BLUE] = Color.BLACK
    blue_objects = find_connected_components(blue_input, background=Color.BLACK, connectivity=4, monochromatic=True)

    red_input = input_grid.copy()
    red_input[input_grid != Color.RED] = Color.BLACK
    red_objects = find_connected_components(red_input, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Extract black holes from blue objects
    holes = [object_interior(obj, background=Color.BLACK) & (obj == Color.BLACK) for obj in blue_objects]
    hole_sprites = [crop(hole, background=Color.BLACK) for hole in holes]

    # Get the red sprites
    red_sprites = [crop(obj, background=Color.BLACK) for obj in red_objects]

    output_grid = np.copy(input_grid)

    for red_sprite, red_obj in zip(red_sprites, red_objects):
        fitted = False
        for hole_sprite, blue_obj in zip(hole_sprites, blue_objects):
            for k in range(4):  # Try all 4 rotations
                rotated_red_sprite = np.rot90(red_sprite, k)
                if np.array_equal(rotated_red_sprite != Color.BLACK, hole_sprite != Color.BLACK):
                    # Remove the red object from its original location
                    output_grid[red_obj != Color.BLACK] = Color.BLACK

                    # Place the rotated red sprite in the hole
                    hole_x, hole_y, _, _ = bounding_box(hole_sprite)
                    blit_sprite(output_grid, rotated_red_sprite, hole_x, hole_y, background=Color.BLACK)

                    fitted = True
                    break
            if fitted:
                break

    return output_grid

def generate_input():
    n, m = np.random.randint(15, 30, size=2)
    input_grid = np.full((n, m), Color.BLACK)

    n_blue_objects = np.random.randint(2, 4)
    for _ in range(n_blue_objects):
        blue_width, blue_height = np.random.randint(6, 10, size=2)
        blue_sprite = np.full((blue_width, blue_height), Color.BLUE)

        # Create a uniquely shaped black hole
        hole_width, hole_height = np.random.randint(2, blue_width-2), np.random.randint(2, blue_height-2)
        hole_sprite = random_sprite(hole_width, hole_height, color_palette=[Color.BLACK], background=Color.BLUE, symmetry="not_symmetric")
        hole_x, hole_y = random_free_location_for_sprite(blue_sprite, hole_sprite, border_size=1, background=Color.BLUE)
        blit_sprite(blue_sprite, hole_sprite, hole_x, hole_y, background=Color.BLUE)

        # Place the blue object in the input grid
        x, y = random_free_location_for_sprite(input_grid, blue_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, blue_sprite, x, y, background=Color.BLACK)

        # Create a matching red object, potentially rotated
        red_sprite = np.full_like(hole_sprite, Color.BLACK)
        red_sprite[hole_sprite == Color.BLACK] = Color.RED
        rotation = np.random.choice([0, 1, 2, 3])
        red_sprite = np.rot90(red_sprite, rotation)

        # Place the red object in the input grid
        x, y = random_free_location_for_sprite(input_grid, red_sprite, padding=1, border_size=1)
        blit_sprite(input_grid, red_sprite, x, y, background=Color.BLACK)

    return input_grid