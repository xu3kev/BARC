from common import *

import numpy as np
from typing import *

# concepts:
# topology, objects, counting, color

# description:
# In the input grid, you will see various colored objects. The goal is to count the number of enclosed regions ("holes") within each object and change the color of the object based on the number of holes:
# - If the object contains 0 holes, color it with RED.
# - If the object contains 1 hole, color it with GREEN.
# - If the object contains 2 holes, color it with BLUE.
# - If the object contains 3 or more holes, color it with YELLOW.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)

    # count the number of enclosed regions within each object
    for obj in objects:
        num_holes = count_holes(obj)
        
        if num_holes == 0:
            color = Color.RED
        elif num_holes == 1:
            color = Color.GREEN
        elif num_holes == 2:
            color = Color.BLUE
        else:
            color = Color.YELLOW

        output_grid[obj != Color.BLACK] = color

    return output_grid

def count_holes(object):
    interior_mask = object_interior(object)
    object_mask = object != Color.BLACK
    hollow_mask = interior_mask & ~object_mask

    if not np.any(hollow_mask):
        return 0

    # Count distinct enclosed regions in hollow_mask
    enclosed_regions = find_connected_components(hollow_mask.astype(int), background=0, connectivity=8, monochromatic=False)
    return len(enclosed_regions)

def generate_input():
    n = np.random.randint(10, 28)
    input_grid = np.full((n, n), Color.BLACK)
    # create random objects. All objects can be hollow or partially hollow or nonhollow.

    def random_hollow_object():
        n, m = np.random.randint(3, 7), np.random.randint(3, 7)
        obj = np.full((n, m), np.random.choice(Color.NOT_BLACK))
        obj[1:n-1, 1:m-1] = Color.BLACK
        return obj

    def random_nonhollow_object():
        obj = random_hollow_object()
        size = np.count_nonzero(obj)
        new_size = np.random.randint(1, size)
        xs, ys = np.where(obj != Color.BLACK)
        for i in range(size - new_size):
            obj[xs[i], ys[i]] = Color.BLACK
        return obj

    def random_mixed_object():
        n, m = np.random.randint(3, 8), np.random.randint(3, 8)
        obj = np.full((n, m), np.random.choice(Color.NOT_BLACK))
        for _ in range(np.random.randint(1, 3)):  # create a random number of holes (up to 2)
            x, y = np.random.randint(1, n-2), np.random.randint(1, m-2)
            hole_size_x, hole_size_y = np.random.randint(1, min(3, n-x)), np.random.randint(1, min(3, m-y))
            obj[x:x+hole_size_x, y:y+hole_size_y] = Color.BLACK
        return obj

    try:
        # add at least one of each type of object and then add random objects until somewhat full
        for _ in range(3):
            obj = random_hollow_object()
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)

        for _ in range(3):
            obj = random_nonhollow_object()
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)
        
        for _ in range(3):
            obj = random_mixed_object()
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)

    except ValueError:
        return generate_input()

    while True:
        obj = random_hollow_object() if np.random.rand() < 0.5 else (random_nonhollow_object() if np.random.rand() < 0.5 else random_mixed_object())
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)
        except ValueError:
            return input_grid