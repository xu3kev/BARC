from common import *

import numpy as np
from typing import *

# concepts:
# filling, topology

# description:
# The input is a black 12x12 grid containing a few grey squares. Each square has a "hole" in it, a contiguous black region of pixels.
# To create the output, fill in the hole of each grey object with red if the hole is a square. Otherwise, leave the hole as is.

def main(input_grid):
    # get the grey squares
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # create an output grid to store the result
    output_grid = np.full(input_grid.shape, Color.BLACK)

    # for each grey square, fill in the hole if it is a square
    for obj in objects:
        # to check if the grey object contains a square hole, we can check if the bounding box of the hole is a square.
        # To do so, first crop the object, then find the black hole inside
        sprite = crop(obj, background=Color.BLACK)
        hole_mask = (sprite == Color.BLACK) & (object_interior(sprite, background=Color.BLACK))

        # check if the mask is square
        def is_square(thing):
            """thing can be a mask or a sprite or an object"""
            thing = crop(thing)
            return np.sum(thing != Color.BLACK) == thing.shape[0] * thing.shape[1] and thing.shape[0] == thing.shape[1]
        
        if is_square(hole_mask):
            sprite[hole_mask] = Color.RED

        # get location of object so we can blit the possibly edited sprite back into the grid
        x, y = object_position(obj, background=Color.BLACK)
        blit_sprite(output_grid, sprite, x, y)

    return output_grid


def generate_input():
    # create a 12x12 black grid
    grid = np.full((12, 12), Color.BLACK)

    # add 2-3 grey squares.
    # For each grey square, add a hole in the middle.
    # 50% chance the hole is a square, otherwise it's a random contiguous object.
    # The hole should not overlap with the border of the square.

    num_grey_squares = np.random.randint(2, 4)

    for _ in range(num_grey_squares):
        # create grey square, and try to find a location for it
        length = np.random.randint(4, 6)
        grey_square = np.full((length, length), Color.GREY)
        try:
            x, y = random_free_location_for_sprite(grid, grey_square, padding=1)
        except ValueError:
            # we were unable to find a space for a square; try over from scratch
            return generate_input()

        # # add a hole in the middle.
        # # 50% chance the hole is a square, otherwise it's a random contiguous object.
        # # The hole should not overlap with the border of the square.
        has_square_hole = np.random.choice([True, False])
        if has_square_hole:
            hole_size = np.random.randint(1, length - 1)
            hole_x, hole_y = np.random.randint(1, length - hole_size), np.random.randint(1, length - hole_size)
            grey_square[hole_x:hole_x + hole_size, hole_y:hole_y + hole_size] = Color.BLACK
        else:
            hole_obj = random_sprite(length-2, length-2, color_palette=[Color.BLACK], background=Color.GREY)
            grey_square[1:-1, 1:-1] = hole_obj

        grid = blit_sprite(grid, grey_square, x, y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)


