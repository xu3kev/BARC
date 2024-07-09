from common import *

import numpy as np
from typing import *

# concepts:
# objects, topology, color change, connectivity

# description:
# In the input grid, you will see various colored objects. Some objects have "holes" (fully-enclosed regions), while others do not.
# To create the output grid:
# 1. For objects with exactly one hole: change their color to green.
# 2. For objects with more than one hole: change their color to yellow.
# 3. For objects with no holes: change their color to red.
# 4. For all objects, fill their holes (if any) with blue.

def main(input_grid):
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8)
    output_grid = np.full_like(input_grid, Color.BLACK)
    
    for obj in objects:
        holes = find_holes(obj)
        num_holes = len(holes)
        
        if num_holes == 1:
            obj[obj != Color.BLACK] = Color.GREEN
        elif num_holes > 1:
            obj[obj != Color.BLACK] = Color.YELLOW
        else:
            obj[obj != Color.BLACK] = Color.RED
        
        blit_object(output_grid, obj, background=Color.BLACK)
        
        for hole in holes:
            hole[hole != Color.BLACK] = Color.BLUE
            blit_object(output_grid, hole, background=Color.BLACK)
    
    return output_grid

def find_holes(obj):
    interior = object_interior(obj)
    obj_mask = obj != Color.BLACK
    hole_mask = interior & ~obj_mask
    hole_components = find_connected_components(hole_mask.astype(int), background=0, connectivity=4)
    return [comp for comp in hole_components if np.any(comp)]

def generate_input():
    n = np.random.randint(20, 30)
    input_grid = np.full((n, n), Color.BLACK)
    
    def random_object_with_holes(num_holes):
        size = np.random.randint(7, 12)
        obj = np.full((size, size), np.random.choice(Color.NOT_BLACK))
        
        for _ in range(num_holes):
            hole_size = np.random.randint(2, 4)
            x = np.random.randint(1, size - hole_size - 1)
            y = np.random.randint(1, size - hole_size - 1)
            obj[x:x+hole_size, y:y+hole_size] = Color.BLACK
        
        return obj
    
    # Ensure we have at least one object of each type (0, 1, and 2+ holes)
    objects = [
        random_object_with_holes(0),
        random_object_with_holes(1),
        random_object_with_holes(np.random.randint(2, 4))
    ]
    
    # Add a few more random objects
    for _ in range(np.random.randint(2, 4)):
        objects.append(random_object_with_holes(np.random.randint(0, 4)))
    
    # Place objects on the grid
    for obj in objects:
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, x=x, y=y)
        except ValueError:
            continue  # Skip if we can't place the object
    
    return input_grid