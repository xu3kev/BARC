from common import *
import numpy as np

# concepts:
# boundary tracing, pixel manipulation

# description:
# In the input you will see a grid containing multiple colored objects.
# To make the output, trace the boundaries of each object and color the boundaries red.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Detect all objects in the input grid
    objects = detect_objects(input_grid, monochromatic=False, connectivity=4)
    
    # Loop through each detected object
    for obj in objects:
        # Compute the boundary of the object
        boundary_mask = object_boundary(obj)
        
        # Set the boundary pixels to RED
        obj[boundary_mask] = Color.RED
        
        # Blit the modified object back to the output grid
        bb = bounding_box(obj)
        blit(output_grid, obj, bb[0], bb[1])

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    num_objects = np.random.randint(1, 4)
    for _ in range(num_objects):
        sprite = random_sprite(np.random.randint(3, 6), np.random.randint(3, 6), color_palette=Color.NOT_BLACK, density=0.5)
        x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK)
        blit(grid, sprite, x, y)

    return grid