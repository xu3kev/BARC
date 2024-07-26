from common import *

import numpy as np
from typing import *


# concepts:
# objects, rotation, transformation

# description:
# In the input you will see several differently colored L-shaped objects on a black background.
# To make the output, rotate each L-shaped object clockwise by 90 degrees from its original orientation.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the L-shaped objects in the input grid
    l_objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=True, connectivity=4, allowed_dimensions=[(3, 3)])

    output_grid = np.copy(input_grid)

    for obj in l_objects:
        # Find the bounding box and crop the object to get the L-shape
        x, y, w, h = bounding_box(obj, background=Color.BLACK)
        l_shape = crop(obj, background=Color.BLACK)
        
        # Rotate L-shape by 90 degrees clockwise
        rotated_l_shape = np.rot90(l_shape, k=3)

        # Remove the original object from the grid
        object_mask = obj != Color.BLACK
        output_grid[object_mask] = Color.BLACK

        # Paste the rotated object at the same position as the original
        blit_sprite(output_grid, rotated_l_shape, x, y, background=Color.BLACK)
        
    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(6, 10, size=2)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(3, 5)

    for _ in range(n_objects):
        color = np.random.choice(list(Color.NOT_BLACK), 1)[0]
        l_shape = np.full((3, 3), Color.BLACK)
        
        orientation = np.random.choice([0, 1, 2, 3])  # Choose a random orientation

        # Create an L-shaped sprite
        l_shape[0, 0] = color
        l_shape[0, 1] = color
        l_shape[0, 2] = color
        l_shape[1, 0] = color
        l_shape = np.rot90(l_shape, k=orientation)

        x, y = random_free_location_for_sprite(grid, l_shape, background=Color.BLACK)
        blit_sprite(grid, l_shape, x, y, background=Color.BLACK)

    return grid