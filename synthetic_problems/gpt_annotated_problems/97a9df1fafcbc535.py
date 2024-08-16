from common import *

import numpy as np
from typing import *

# concepts:
# direction, lines, color, uniqueness

# description:
# In the input, you will see several colored objects, each in the shape of an "L".
# One color appears only once (the unique color).
# For each non-unique colored L, draw a line from its corner in the direction it's pointing.
# The line should be the same color as the L and should stop when it hits another object or the edge of the grid.
# For the unique colored L, draw a line in the opposite direction it's pointing.

def main(input_grid):
    output_grid = np.copy(input_grid)
    objects = find_connected_components(input_grid, connectivity=8)
    
    # Find the unique color
    color_counts = {}
    for obj in objects:
        color = np.unique(obj[obj != Color.BLACK])[0]
        color_counts[color] = color_counts.get(color, 0) + 1
    unique_color = [c for c, count in color_counts.items() if count == 1][0]

    for obj in objects:
        x, y, w, h = bounding_box(obj)
        sprite = crop(obj)
        color = np.unique(obj[obj != Color.BLACK])[0]
        
        # Determine L direction (assuming L shape is always 2x2)
        if sprite[0, 0] == Color.BLACK:
            direction = (1, 1)  # pointing down-right
        elif sprite[0, 1] == Color.BLACK:
            direction = (1, -1)  # pointing down-left
        elif sprite[1, 0] == Color.BLACK:
            direction = (-1, 1)  # pointing up-right
        else:
            direction = (-1, -1)  # pointing up-left

        # For unique color, reverse the direction
        if color == unique_color:
            direction = (-direction[0], -direction[1])

        # Find starting point (the corner of the L)
        start_x = x + (0 if direction[0] > 0 else w - 1)
        start_y = y + (0 if direction[1] > 0 else h - 1)

        # Draw the line
        draw_line(output_grid, start_x, start_y, length=None, color=color, direction=direction, stop_at_color=Color.NOT_BLACK)

    return output_grid

def generate_input():
    grid = np.zeros((12, 12), dtype=int)
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)
    
    for i in range(min(5, len(colors))):
        color = colors[i]
        # Create L shape
        l_shape = np.full((2, 2), color)
        corner = np.random.randint(4)
        l_shape[corner // 2, corner % 2] = Color.BLACK
        
        # Place L shape
        x, y = random_free_location_for_sprite(grid, l_shape, padding=1)
        blit_sprite(grid, l_shape, x=x, y=y)
        
        # For non-unique colors, add another instance
        if i > 0:
            x, y = random_free_location_for_sprite(grid, l_shape, padding=1)
            blit_sprite(grid, l_shape, x=x, y=y)

    return grid