from common import *

import numpy as np
from typing import *

# concepts:
# colors, objects, pixel manipulation

# description:
# In the input, you will see various colored objects on a black background.
# To create the output, for each object, replace its color with the next color in the sequence:
# RED -> GREEN -> BLUE -> YELLOW -> ORANGE -> PINK -> RED
# Any other colors should remain unchanged.

def main(input_grid):
    output_grid = input_grid.copy()
    
    color_sequence = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK]
    color_map = {color: color_sequence[(i + 1) % len(color_sequence)] for i, color in enumerate(color_sequence)}
    
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)
    
    for obj in objects:
        color = np.unique(obj)[1]  # Get the color of the object
        if color in color_map:
            new_color = color_map[color]
            output_grid[obj != Color.BLACK] = new_color
    
    return output_grid

def generate_input():
    grid_size = np.random.randint(10, 20)
    input_grid = np.zeros((grid_size, grid_size), dtype=int)
    
    colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK, Color.TEAL, Color.MAROON]
    num_objects = np.random.randint(3, 7)
    
    for _ in range(num_objects):
        color = np.random.choice(colors)
        sprite = random_sprite(n=[3, 4, 5], m=[3, 4, 5], color_palette=[color])
        x, y = random_free_location_for_sprite(input_grid, sprite, padding=1)
        blit_sprite(input_grid, sprite, x, y)
    
    return input_grid