from common import *
import numpy as np
import random
from typing import *

# concepts:
# sliding objects, symmetries, connecting colors

# description:
# In the input grid, there will be a colored symmetrical object and several pairs of points of the same color.
# The task is to slide the object to ensure that one of its symmetrical points intersects with the same-colored pair points.
# The object should be slid in such a way that once it intersects with one of the pair points, it should preserve its symmetry.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Extract the symmetrical object and the colored pair points.
    # 2. Determine all possible symmetrical variations of the object.
    # 3. Slide the object in the grid to ensure that at least one symmetrical point intersects with a pair point of the same color.
    # 4. The output grid will reflect the transformed state.

    # Find the symmetrical object and colored pair points
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=4)

    # Assuming the symmetrical object will be the largest or the most complex
    sym_obj = max(objects, key=lambda obj: obj.size)

    # The color pairs will be those not part of the symmetrical object.
    color_pairs = [point for point in objects if point is not sym_obj]

    # Generating symmetrical variations of the object
    sym_varieties = [
        sym_obj,
        np.rot90(sym_obj),
        np.rot90(sym_obj, 2),
        np.rot90(sym_obj, 3),
        np.flipud(sym_obj),
        np.fliplr(sym_obj),
        np.flipud(np.rot90(sym_obj)),
        np.fliplr(np.rot90(sym_obj))
    ]

    output_grid = np.copy(input_grid)

    for variant in sym_varieties:
        for pair in color_pairs:
            pair_color = next(iter(set(pair.flatten()) - {Color.BLACK}))
            if np.any((variant != Color.BLACK) & (pair == pair_color)):
                blit_object(output_grid, variant, background=Color.BLACK)
                return output_grid

    return output_grid


def generate_input():
    # make a black grid as background
    n, m = random.randint(10, 15), random.randint(10, 15)
    grid = np.full((n, m), Color.BLACK)

    # Create a symmetrical object
    sym_obj = random_sprite(np.random.randint(3, 5), np.random.randint(3, 5), symmetry="horizontal", color_palette=Color.NOT_BLACK)

    # Place the symmetrical object somewhere random
    x, y = random_free_location_for_sprite(grid, sym_obj, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, sym_obj, x, y, background=Color.BLACK)

    # Create several pairs of points
    num_pairs = np.random.randint(2, 5)
    for _ in range(num_pairs):
        pair_color = random.choice(Color.NOT_BLACK)
        x1, y1 = random_free_location_for_sprite(grid, np.array([[pair_color]]), background=Color.BLACK, padding=1, border_size=1)
        x2, y2 = random_free_location_for_sprite(grid, np.array([[pair_color]]), background=Color.BLACK, padding=1, border_size=1)
        grid[x1, y1] = pair_color
        grid[x2, y2] = pair_color

    return grid