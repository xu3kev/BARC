from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, color mapping, sprites

# description:
# The input is a grid containing several objects (sprites). Each sprite has a unique color and one or more axes of symmetry (horizontal, vertical, diagonal, or radial). Each symmetrical sprite is assigned a color according to a predefined color mapping (green -> yellow, blue -> gray, red -> pink, teal -> maroon, yellow -> green, gray -> blue, pink -> red, maroon -> teal). The task is to identify each symmetrical sprite, apply the color mapping, and return the modified grid.

color_map = {
    Color.GREEN: Color.YELLOW,
    Color.BLUE: Color.GRAY,
    Color.RED: Color.PINK,
    Color.TEAL: Color.MAROON,
    Color.YELLOW: Color.GREEN,
    Color.GRAY: Color.BLUE,
    Color.PINK: Color.RED,
    Color.MAROON: Color.TEAL             
}

def main(input_grid):
    # Create a copy of the input grid to work on
    output_grid = input_grid.copy()
    
    # Identify all objects in the grid
    objects = find_connected_components(input_grid, connectivity=8)

    for obj in objects:
        # Crop the object to isolate it as a sprite
        sprite = crop(obj)
        
        # Determine if the object is symmetric
        is_symmetric = is_sprite_symmetric(sprite)
        
        if is_symmetric:
            # Get the main color of the sprite (exclude background)
            unique_colors = np.unique(sprite)
            main_color = unique_colors[unique_colors != Color.BLACK][0]
            
            # Apply color mapping
            if main_color in color_map:
                sprite[sprite == main_color] = color_map[main_color]
                
            # Get object's original position in the output grid
            x, y, _, _ = bounding_box(obj)
            
            # Place the modified sprite back in the output grid
            blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)
    
    return output_grid

def is_sprite_symmetric(sprite):
    # Check for different types of symmetry in the sprite
    if np.array_equal(sprite, np.rot90(sprite, 1)):
        return True
    elif np.array_equal(sprite, np.fliplr(sprite)):
        return True
    elif np.array_equal(sprite, np.flipud(sprite)):
        return True
    elif np.array_equal(sprite, sprite.T) or np.array_equal(np.flipud(sprite), np.fliplr(sprite)):
        return True
    return False

def generate_input():
    # Create a black background grid
    grid_size = 10
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Generate and place symmetric sprites
    for _ in range(np.random.randint(3, 6)):
        color = np.random.choice(list(Color.NOT_BLACK))
        side_length = np.random.randint(2, 8)
        symmetry = np.random.choice(['vertical', 'horizontal', 'diagonal', 'radial'])
        sprite = random_sprite(side_length, side_length, symmetry=symmetry, color_palette=[color], connectivity=8)
        
        # Place sprite on the grid, ensuring no collisions
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1)
            blit_sprite(grid, sprite, x, y)
        except:
            pass

    return grid