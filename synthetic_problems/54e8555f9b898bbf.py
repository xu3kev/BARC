from common import *

import numpy as np
from typing import *

# concepts:
# Symmetry, Object detection, Cropping

# description:
# In the input grid, you will see several objects of different colors scattered around a black grid.
# Your task is to find all objects with reflective symmetry. 
# Then crop the objects to their smallest bounding boxes and place them at the top of the grid.
# Arrange these objects horizontally in the output grid, without any gaps in-between.

def main(input_grid):
    # Find all objects in the grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    # Filter objects that have reflective symmetry
    symmetrical_objects = []
    for obj in objects:
        symmetries = detect_mirror_symmetry(obj, ignore_colors=[Color.BLACK])
        if symmetries:
            symmetrical_objects.append(crop(obj, background=Color.BLACK))

    # Create a large enough output grid
    output_grid_height = max([obj.shape[0] for obj in symmetrical_objects]) if symmetrical_objects else 1
    total_width = sum([obj.shape[1] for obj in symmetrical_objects]) if symmetrical_objects else 1
    output_grid = np.full((output_grid_height, total_width), Color.BLACK)

    # Add the symmetrical objects to the output grid, horizontally concatenated
    current_x = 0
    for obj in symmetrical_objects:
        h, w = obj.shape
        output_grid[:h, current_x:current_x+w] = obj
        current_x += w

    return output_grid


def generate_input():
    # Create a 10x10 empty grid (black background)
    n, m = 10, 10
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Generate random objects with or without symmetry
    symmetrical_choices = [True, False]
    for _ in range(np.random.randint(2, 5)):
        width, height = np.random.randint(2, 4, size=2)
        is_symmetric = np.random.choice(symmetrical_choices)

        # Select a color for the object
        obj_color = random.choice(Color.NOT_BLACK)

        # Create a random sprite
        sprite = random_sprite(width, height, color_palette=[obj_color], symmetry=('horizontal' if is_symmetric else 'not_symmetric'))

        # Find a random free location for the object in the grid, ensure no overlap
        x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK, padding=1)
        if x is not None and y is not None:
            blit(grid, sprite, x, y)

    return grid