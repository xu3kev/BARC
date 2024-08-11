from common import *

import numpy as np
from typing import *

# concepts:
# objects, topology, counting

# description:
# The input grid contains various blue objects. Each object has a color-coded interior: red, green, yellow, or black.
# The transformation involves counting the number of objects for each viable interior color (excluding black) and representing them in a newly formatted output grid.
# The output grid consists of colored strips: each stripâs width represents the count of objects with respective interior color.
 
def main(input_grid):
    output_grid = np.zeros_like(input_grid)
    objects = find_connected_components(input_grid, connectivity=4)

    # Store counts of different interior colors
    color_counts = { color: 0 for color in [Color.RED, Color.GREEN, Color.YELLOW] }
    
    for obj in objects:
        # Check interior color of the object
        interior_color = identify_interior_color(obj)
        if interior_color in color_counts:
            color_counts[interior_color] += 1
    
    # Create the output grid using the counts
    current_position = 0
    output_shape = list(input_grid.shape)
    for color, count in color_counts.items():
        # Skip if no objects of this color
        if count == 0:
            continue
        
        # Draw vertical strip representing count of the current color
        for y in range(current_position, current_position + count):
            if y < output_shape[1]:
                output_grid[:, y] = color

        current_position += count
    
    return output_grid

def identify_interior_color(obj):
    interior_mask = object_interior(obj)
    colors_inside = obj[interior_mask & (obj != Color.BLACK)]
    
    if len(colors_inside) == 0:
        return None
    
    # Assuming the interior should have a uniform color 
    unique_colors, counts = np.unique(colors_inside, return_counts=True)
    main_color = unique_colors[np.argmax(counts)]
    
    return main_color

def generate_input():
    n = np.random.randint(10, 28)
    input_grid = np.full((n, n), Color.BLACK)

    def random_hollow_object_with_interior(interior_color):
        h, w = np.random.randint(3, 7), np.random.randint(3, 7)
        obj = np.full((h, w), Color.BLUE)
        obj[1:h-1, 1:w-1] = interior_color
        return obj

    viable_colors = [Color.RED, Color.GREEN, Color.YELLOW]
    
    while True:
        for color in viable_colors:
            try:
                obj = random_hollow_object_with_interior(color)
                x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
                blit_sprite(input_grid, obj, x=x, y=y)
            except ValueError:
                return input_grid

        if np.any(input_grid == Color.BLUE):
            return input_grid

        # If no blue pixels found, re-generate input
        input_grid = np.full((n, n), Color.BLACK)

    return input_grid