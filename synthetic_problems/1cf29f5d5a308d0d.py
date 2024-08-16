from common import *

import numpy as np
from typing import *

# concepts:
# objects, topology, counting, sliding objects

# description:
# In the input grid, you will see various blue objects. Some are "hollow" and contain a fully-enclosed region, while others do not have a middle that is separate from outside the object, and fully enclosed.
# For each hollow object, count the number of non-hollow objects that could fit inside its hollow region if slid into place.
# To create the output grid, copy the input grid. Then, change the color of each hollow object based on this count:
# - If 0 non-hollow objects fit, change to red
# - If 1 non-hollow object fits, change to yellow
# - If 2 or more non-hollow objects fit, change to green

def main(input_grid):
    objects = find_connected_components(input_grid, connectivity=4)
    output_grid = input_grid.copy()
    
    hollow_objects = []
    non_hollow_objects = []
    
    for obj in objects:
        if is_hollow(obj):
            hollow_objects.append(obj)
        else:
            non_hollow_objects.append(obj)
    
    for hollow_obj in hollow_objects:
        count = count_fitting_objects(hollow_obj, non_hollow_objects)
        if count == 0:
            new_color = Color.RED
        elif count == 1:
            new_color = Color.YELLOW
        else:
            new_color = Color.GREEN
        
        hollow_obj[hollow_obj != Color.BLACK] = new_color
        blit_object(output_grid, hollow_obj, background=Color.BLACK)
    
    return output_grid

def is_hollow(object):
    interior_mask = object_interior(object)
    object_mask = object != Color.BLACK
    hollow_mask = interior_mask & ~object_mask
    return np.any(hollow_mask)

def count_fitting_objects(hollow_obj, non_hollow_objects):
    interior = object_interior(hollow_obj) & (hollow_obj == Color.BLACK)
    count = 0
    for obj in non_hollow_objects:
        if fits_inside(obj, interior):
            count += 1
    return count

def fits_inside(obj, interior):
    obj_mask = obj != Color.BLACK
    for x in range(interior.shape[0] - obj.shape[0] + 1):
        for y in range(interior.shape[1] - obj.shape[1] + 1):
            if np.all(interior[x:x+obj.shape[0], y:y+obj.shape[1]][obj_mask]):
                return True
    return False

def generate_input():
    n = np.random.randint(15, 30)
    input_grid = np.full((n, n), Color.BLACK)

    def random_hollow_object():
        n, m = np.random.randint(5, 10), np.random.randint(5, 10)
        obj = np.full((n, m), Color.BLUE)
        obj[1:n-1, 1:m-1] = Color.BLACK
        return obj

    def random_nonhollow_object():
        n, m = np.random.randint(2, 5), np.random.randint(2, 5)
        obj = np.full((n, m), Color.BLUE)
        # Remove a random number of pixels
        pixels_to_remove = np.random.randint(1, n*m // 2)
        for _ in range(pixels_to_remove):
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            obj[x, y] = Color.BLACK
        return obj

    # Add 2-4 hollow objects
    for _ in range(np.random.randint(2, 5)):
        obj = random_hollow_object()
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)
        except ValueError:
            continue

    # Add 3-6 non-hollow objects
    for _ in range(np.random.randint(3, 7)):
        obj = random_nonhollow_object()
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)
        except ValueError:
            continue

    return input_grid