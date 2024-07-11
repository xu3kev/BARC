from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, topology, repeating pattern

# description:
# In the input grid, you will see a U-shaped object of one color and several smaller objects of another color, all on a black background.
# To produce the output grid:
# 1. Slide all smaller objects downward until they either touch the bottom of the grid or the top of the U-shaped object.
# 2. For each smaller object that ends up inside the U-shape:
#    a. Determine if the object is "hollow" (contains a fully-enclosed region).
#    b. If it is hollow, create a repeating pattern inside the U-shape above the object:
#       alternate horizontal lines of the U-shape's color and the smaller object's color,
#       starting from the top of the smaller object and extending to the top of the U-shape.
#    c. If it is not hollow, leave it as is.
# 3. Remove any smaller objects that did not end up inside the U-shape.

def main(input_grid):
    output_grid = input_grid.copy()
    
    # Find the U-shaped object (largest object)
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    u_shape = max(objects, key=lambda o: np.count_nonzero(o))
    u_color = u_shape[u_shape != Color.BLACK][0]
    
    # Find the color of the smaller objects
    colors = set(np.unique(input_grid)) - {Color.BLACK, u_color}
    assert len(colors) == 1
    small_color = colors.pop()
    
    # Find and process smaller objects
    small_objects = [obj for obj in objects if obj[obj != Color.BLACK][0] == small_color]
    
    for obj in small_objects:
        # Slide object downward
        obj_coords = np.argwhere(obj != Color.BLACK)
        min_y, max_y = obj_coords[:, 1].min(), obj_coords[:, 1].max()
        x = obj_coords[0, 0]  # Assuming the object is vertically aligned
        
        # Find landing position
        landing_y = output_grid.shape[1] - 1
        for y in range(max_y + 1, output_grid.shape[1]):
            if output_grid[x, y] != Color.BLACK:
                landing_y = y - 1
                break
        
        # Move object to landing position
        shift = landing_y - max_y
        new_obj = np.roll(obj, shift, axis=1)
        
        # Check if object is inside U-shape
        if is_inside_u_shape(new_obj, u_shape):
            if is_hollow(new_obj):
                # Create repeating pattern above hollow object
                top_of_object = np.argwhere(new_obj != Color.BLACK)[:, 1].min()
                for y in range(top_of_object - 1, -1, -1):
                    if u_shape[x, y] == u_color:
                        output_grid[x, y] = small_color if y % 2 == 0 else u_color
                    else:
                        break
            # Blit the object onto the output grid
            blit_object(output_grid, new_obj, background=Color.BLACK)
        else:
            # Remove object if not inside U-shape
            output_grid[new_obj != Color.BLACK] = Color.BLACK
    
    return output_grid

def is_inside_u_shape(obj, u_shape):
    obj_coords = np.argwhere(obj != Color.BLACK)
    x, y = obj_coords[0, 0], obj_coords[:, 1].min()  # Top of the object
    return u_shape[x, y-1] != Color.BLACK if y > 0 else False

def is_hollow(object):
    interior_mask = object_interior(object)
    object_mask = object != Color.BLACK
    hollow_mask = interior_mask & ~object_mask
    return np.any(hollow_mask)

def generate_input():
    grid_size = np.random.randint(20, 29)
    input_grid = np.full((grid_size, grid_size), Color.BLACK)
    
    # Choose colors
    u_color, small_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)
    
    # Create U-shape
    u_width = np.random.randint(8, 13)
    u_height = np.random.randint(12, 17)
    u_thickness = np.random.randint(2, 4)
    u_shape = np.full((u_height, u_width), Color.BLACK)
    u_shape[:, :u_thickness] = u_color
    u_shape[:, -u_thickness:] = u_color
    u_shape[-u_thickness:, :] = u_color
    
    # Place U-shape
    x = np.random.randint(0, grid_size - u_height)
    y = np.random.randint(0, grid_size - u_width)
    blit_sprite(input_grid, u_shape, x, y)
    
    # Create and place smaller objects
    for _ in range(np.random.randint(3, 7)):
        obj_height = np.random.randint(3, 6)
        obj_width = np.random.randint(2, 4)
        obj = np.full((obj_height, obj_width), small_color)
        
        if np.random.random() < 0.5:  # Make some objects hollow
            obj[1:-1, 1:-1] = Color.BLACK
        
        try:
            obj_x, obj_y = random_free_location_for_sprite(input_grid, obj, padding=1)
            blit_sprite(input_grid, obj, obj_x, obj_y)
        except ValueError:
            continue  # Skip if can't place
    
    return input_grid