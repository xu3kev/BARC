from common import *

import numpy as np
from typing import *

# concepts:
# boundary tracing, color mapping

# description:
# The input consists of a grid containing multiple objects with different color boundaries.
# Transform the input by detecting each object's boundary and filling the object's interior with a color based on the boundary's color.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Initialize output grid
    output_grid = input_grid.copy()
    
    # Find the connected components in the grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8)
    
    for obj in objects:
        # Detect the boundary of the object
        boundary = object_boundary(obj, background=Color.BLACK)
        
        # Get the boundary's color
        boundary_colors = set(input_grid[boundary])
        
        if len(boundary_colors) != 1:
            raise ValueError("Object boundary must be of a single color.")
        
        boundary_color = next(iter(boundary_colors))
        
        # Perform color mapping
        fill_color = color_map[boundary_color]
        
        # Detect the interior of the object
        interior = object_interior(obj, background=Color.BLACK)
        
        # Fill the interior with the fill color
        output_grid[interior] = fill_color
    
    return output_grid
    
# Constructing the color map for boundary to interior fill
color_map = {
    Color.RED: Color.GREEN,
    Color.BLUE: Color.YELLOW,
    Color.GREEN: Color.RED,
    Color.YELLOW: Color.BLUE,
    Color.MAROON: Color.TEAL,
    Color.TEAL: Color.MAROON,
    Color.PINK: Color.ORANGE,
    Color.ORANGE: Color.PINK,
    Color.GREY: Color.BLACK,
    Color.BLACK: Color.GREY,
}

def generate_input():
    # Randomly decide the dimensions of the grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)
    
    # Create several objects with different boundary colors
    num_objects = np.random.randint(3, 6)  # Number of objects
    
    for _ in range(num_objects):
        # Decide dimensions and color for the object
        obj_width, obj_height = np.random.randint(3, 6), np.random.randint(3, 6)
        boundary_color = np.random.choice(list(color_map.keys()))
        
        # Create an empty object with the same dimensions
        obj = np.full((obj_width, obj_height), Color.BLACK, dtype=int)
        
        # Draw the boundary with boundary_color
        obj[0,:] = boundary_color
        obj[-1,:] = boundary_color
        obj[:,0] = boundary_color
        obj[:,-1] = boundary_color
        
        # Place the object in a random spot in the grid
        try:
            x, y = random_free_location_for_object(grid, obj, background=Color.BLACK)
        except:
            continue
        
        blit(grid, obj, x, y, background=Color.BLACK)
    
    return grid