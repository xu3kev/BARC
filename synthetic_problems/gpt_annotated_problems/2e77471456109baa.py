from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, collision detection, direction, magnetism

# description:
# In the input, you will see a blue 2x2 square and several red 1x1 pixels scattered around the grid.
# The blue square acts as a magnet, attracting all red pixels.
# Slide each red pixel towards the blue square until it touches either the blue square or another red pixel that has already moved.
# The order of movement is determined by the distance to the blue square, with the closest red pixel moving first.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find the blue square
    blue_coords = np.argwhere(input_grid == Color.BLUE)
    blue_center = blue_coords.mean(axis=0).astype(int)
    
    # Find all red pixels
    red_pixels = np.argwhere(input_grid == Color.RED)
    
    # Calculate distances of red pixels to the blue square center
    distances = np.linalg.norm(red_pixels - blue_center, axis=1)
    
    # Sort red pixels by distance
    sorted_indices = np.argsort(distances)
    
    for idx in sorted_indices:
        x, y = red_pixels[idx]
        
        # Determine direction towards blue square
        dx = np.sign(blue_center[0] - x)
        dy = np.sign(blue_center[1] - y)
        
        # Slide the red pixel
        while True:
            new_x, new_y = x + dx, y + dy
            
            # Check if the new position is valid
            if (new_x < 0 or new_x >= input_grid.shape[0] or 
                new_y < 0 or new_y >= input_grid.shape[1]):
                break
            
            # Check if the new position touches blue or another red
            if contact(object1=output_grid, object2=np.array([[Color.RED]]), x2=new_x, y2=new_y):
                break
            
            # Move the red pixel
            output_grid[x, y] = Color.BLACK
            output_grid[new_x, new_y] = Color.RED
            x, y = new_x, new_y
    
    return output_grid

def generate_input():
    # Create a black grid
    n, m = random.randint(8, 15), random.randint(8, 15)
    grid = np.full((n, m), Color.BLACK)
    
    # Place the blue square
    blue_square = np.full((2, 2), Color.BLUE)
    bx, by = random_free_location_for_sprite(grid, blue_square, padding=1, border_size=1)
    blit_sprite(grid, blue_square, bx, by)
    
    # Place red pixels
    red_pixel = np.array([[Color.RED]])
    for _ in range(random.randint(3, 7)):
        rx, ry = random_free_location_for_sprite(grid, red_pixel, padding=1)
        blit_sprite(grid, red_pixel, rx, ry)
    
    return grid