from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, collision avoidance, objects

# description:
# In the input, you will see one or more multicolored objects on a grid. Each object needs to slide to the right by one pixel unless blocked by another object. If an object hits an obstacle, it will stop.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract objects from the input grid
    objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=False, connectivity=8)
    
    n, m = input_grid.shape
    output_grid = np.full((n, m), Color.BLACK)

    for obj in objects:
        # Crop the object to get its non-background portion
        cropped_object = crop(obj)

        # Detect the current position of the object
        x, y, _, _ = bounding_box(cropped_object, background=Color.BLACK)
        
        # Check if we can slide the object to the right by one pixel
        can_slide = True
        new_x, new_y = x, y + 1
        for i in range(cropped_object.shape[0]):
            for j in range(cropped_object.shape[1]):
                if cropped_object[i, j] != Color.BLACK:
                    if new_y + j >= m or input_grid[i + x, j + y + 1] != Color.BLACK:
                        can_slide = False
                        break
            if not can_slide:
                break
        
        if can_slide:
            new_y = y + 1
        
        # Update the output grid with the (possibly moved) object
        blit(output_grid, cropped_object, new_x, new_y, background=Color.BLACK)
    
    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.full((n, m), Color.BLACK)
    
    num_objects = np.random.randint(2, 4)
    for _ in range(num_objects):
        sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=random.sample(list(Color.NOT_BLACK), np.random.randint(1, 4)))
        x, y = random_free_location_for_object(grid, sprite, padding=1)
        blit(grid, sprite, x, y)
    
    return grid