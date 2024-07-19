from common import *

import numpy as np
import random
from typing import *

# concepts:
# decomposition, counting, color change

# description:
# In the input, you will see a black canvas scattered with shapes of size either 2x3, 3x2 or 3x3. 
# These shapes could be of any color except black. Each shape should be treated as a separate entity.
# The goal is to count the number of each type of shape, and make a 3xN grid where N is the number of shapes detected:
# 1. All 2x3 shapes will be colored yellow
# 2. All 3x2 shapes will be colored blue
# 3. All 3x3 shapes will be colored green
# Shapes should appear in the grid in the above order (2x3, 3x2, 3x3).

def main(input_grid: np.ndarray) -> np.ndarray:
    
    shapes_2x3 = []
    shapes_3x2 = []
    shapes_3x3 = []
    
    objects = detect_objects(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    for obj in objects:
        obj_bb = crop(obj, background=Color.BLACK)
        h, w = obj_bb.shape
        
        if (h, w) == (2, 3):
            obj_bb[:, :] = Color.YELLOW
            shapes_2x3.append(obj_bb)
        elif (h, w) == (3, 2):
            obj_bb[:, :] = Color.BLUE
            shapes_3x2.append(obj_bb)
        elif (h, w) == (3, 3):
            obj_bb[:, :] = Color.GREEN
            shapes_3x3.append(obj_bb)
    
    total_shapes = len(shapes_2x3) + len(shapes_3x2) + len(shapes_3x3)
    
    output_grid = np.full((3, 3 * total_shapes), Color.BLACK)
    
    x = 0
    for shape in shapes_2x3 + shapes_3x2 + shapes_3x3:
        blit_sprite(output_grid, shape, 0, x)
        x += max(shape.shape)
    
    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(15, 20), np.random.randint(15, 20)
    grid = np.full((n, m), Color.BLACK)

    colors_to_use = list(Color.NOT_BLACK)
    shapes = [(2, 3), (3, 2), (3, 3)]
    
    for _ in range(np.random.randint(10, 15)):
        color = random.choice(colors_to_use)
        shape_size = random.choice(shapes)
        shape = np.full(shape_size, color)
        
        try:
            x, y = random_free_location_for_sprite(grid, shape, background=Color.BLACK, padding=1, padding_connectivity=8)
        except:
            continue
            
        blit_sprite(grid, shape, x, y, background=Color.BLACK)
    
    return grid