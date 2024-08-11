from common import *

import numpy as np
from typing import *

# concepts:
# bitmasks with separator, boolean logical operations, objects, color

# description:
# In the input, you will see a grid divided into three sections by two horizontal yellow lines. 
# The top and bottom sections contain red and blue objects on a black background.
# The middle section contains green objects on a black background.
# To make the output:
# 1. Overlay the top and bottom sections using the AND operation (both must be colored).
# 2. For each green object in the middle section:
#    - If it touches (4-connected) any pixel from the AND result, color it orange.
#    - Otherwise, leave it green.
# 3. The final output should only contain the modified middle section.

def main(input_grid):
    width, height = input_grid.shape
    
    # Find the yellow horizontal lines
    yellow_lines = [y for y in range(height) if np.all(input_grid[:, y] == Color.YELLOW)]
    top_section = input_grid[:, :yellow_lines[0]]
    middle_section = input_grid[:, yellow_lines[0]+1:yellow_lines[1]]
    bottom_section = input_grid[:, yellow_lines[1]+1:]
    
    # Perform AND operation on top and bottom sections
    and_result = np.logical_and(
        np.logical_or(top_section == Color.RED, top_section == Color.BLUE),
        np.logical_or(bottom_section == Color.RED, bottom_section == Color.BLUE)
    )
    
    # Create output grid (same size as middle section)
    output_grid = np.copy(middle_section)
    
    # Find green objects in the middle section
    green_objects = find_connected_components(middle_section, background=Color.BLACK)
    
    # Check each green object
    for obj in green_objects:
        # Create a padded version of the object to check for neighbors
        padded_obj = np.pad(obj, pad_width=1, mode='constant', constant_values=Color.BLACK)
        
        # Check if any pixel of the object touches the AND result
        touches_and_result = False
        for x in range(1, padded_obj.shape[0] - 1):
            for y in range(1, padded_obj.shape[1] - 1):
                if padded_obj[x, y] == Color.GREEN:
                    # Check 4-connected neighbors
                    neighbors = [
                        (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                    ]
                    for nx, ny in neighbors:
                        if 0 <= nx-1 < and_result.shape[0] and 0 <= ny-1 < and_result.shape[1]:
                            if and_result[nx-1, ny-1]:
                                touches_and_result = True
                                break
                    if touches_and_result:
                        break
            if touches_and_result:
                break
        
        # Color the object orange if it touches the AND result
        if touches_and_result:
            output_grid[obj == Color.GREEN] = Color.ORANGE
    
    return output_grid

def generate_input():
    width = 10
    height = 15
    
    input_grid = np.full((width, height), Color.BLACK)
    
    # Create yellow separator lines
    line1 = np.random.randint(4, 6)
    line2 = np.random.randint(9, 11)
    input_grid[:, line1] = Color.YELLOW
    input_grid[:, line2] = Color.YELLOW
    
    # Generate objects for top and bottom sections
    for section in [input_grid[:, :line1], input_grid[:, line2+1:]]:
        num_objects = np.random.randint(2, 5)
        for _ in range(num_objects):
            color = np.random.choice([Color.RED, Color.BLUE])
            obj = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=[color])
            x, y = random_free_location_for_sprite(section, obj)
            blit_sprite(section, obj, x, y)
    
    # Generate green objects for middle section
    middle_section = input_grid[:, line1+1:line2]
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        obj = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=[Color.GREEN])
        x, y = random_free_location_for_sprite(middle_section, obj)
        blit_sprite(middle_section, obj, x, y)
    
    return input_grid