from common import *

import numpy as np
from typing import *

# concepts:
# objects, counting, color, topology

# description:
# In the input, you will see colored objects on a black background.
# To make the output:
# 1. Count the number of holes in each object.
# 2. Color the object red if it has no holes, green if it has one hole, and blue if it has two or more holes.
# 3. If an object contains another object inside one of its holes, color the inner object yellow.

def main(input_grid):
    output_grid = np.copy(input_grid)
    objects = find_connected_components(input_grid, background=Color.BLACK)

    for obj in objects:
        hole_count = count_holes(obj)
        if hole_count == 0:
            color = Color.RED
        elif hole_count == 1:
            color = Color.GREEN
        else:
            color = Color.BLUE
        
        output_grid[obj != Color.BLACK] = color

    # Check for objects inside holes
    for outer_obj in objects:
        inner_objects = find_inner_objects(outer_obj, objects)
        for inner_obj in inner_objects:
            output_grid[inner_obj != Color.BLACK] = Color.YELLOW

    return output_grid

def count_holes(obj):
    interior = object_interior(obj, background=Color.BLACK)
    holes = find_connected_components(~interior & (obj == Color.BLACK), background=True)
    return len(holes) - 1  # Subtract 1 to exclude the outer background

def find_inner_objects(outer_obj, all_objects):
    interior = object_interior(outer_obj, background=Color.BLACK)
    inner_objects = []
    for obj in all_objects:
        if obj is not outer_obj and np.all((obj != Color.BLACK) <= interior):
            inner_objects.append(obj)
    return inner_objects

def generate_input():
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.full((n, m), Color.BLACK)

    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)

    for _ in range(np.random.randint(3, 6)):
        obj_size = np.random.randint(5, 10)
        obj = random_sprite(obj_size, obj_size, density=0.7, color_palette=[colors.pop()])
        
        # Add holes
        num_holes = np.random.randint(0, 3)
        for _ in range(num_holes):
            hole_size = np.random.randint(2, 4)
            hole = np.full((hole_size, hole_size), Color.BLACK)
            x, y = random_free_location_for_sprite(obj, hole, background=Color.BLACK)
            blit_sprite(obj, hole, x, y)
        
        # Sometimes add an inner object
        if num_holes > 0 and np.random.random() < 0.5:
            inner_obj = random_sprite(3, 3, density=0.8, color_palette=[colors.pop()])
            interior = object_interior(obj, background=Color.BLACK)
            valid_positions = np.argwhere((interior == 1) & (obj == Color.BLACK))
            if len(valid_positions) > 0:
                x, y = valid_positions[np.random.randint(len(valid_positions))]
                blit_sprite(obj, inner_obj, x, y)

        try:
            x, y = random_free_location_for_sprite(grid, obj, padding=1)
            blit_sprite(grid, obj, x, y)
        except ValueError:
            pass

    return grid