from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, repeating pattern, connecting colors

# description:
# In the input, you will see two colored pixels of different colors on a black background.
# To make the output, draw diagonal lines connecting these two pixels, alternating between the two colors.
# The lines should be drawn in a zigzag pattern, changing direction at each step.
# The zigzag should have a consistent step size, which is determined by the distance between the two pixels.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find the two colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    assert len(colored_pixels) == 2, "Input should have exactly two colored pixels"
    
    # Extract coordinates and colors
    (x1, y1), (x2, y2) = colored_pixels
    color1, color2 = input_grid[x1, y1], input_grid[x2, y2]
    
    # Calculate step size (Manhattan distance divided by 4, minimum 1)
    step_size = max(1, (abs(x2 - x1) + abs(y2 - y1)) // 4)
    
    # Initialize starting point and direction
    x, y = x1, y1
    dx, dy = np.sign(x2 - x1), np.sign(y2 - y1)
    
    # Draw zigzag pattern
    current_color = color1
    while (x, y) != (x2, y2):
        # Draw horizontal part of zigzag
        end_x = min(x2, max(x1, x + dx * step_size)) if dx > 0 else max(x2, min(x1, x + dx * step_size))
        draw_line(output_grid, x, y, length=abs(end_x - x), color=current_color, direction=(dx, 0))
        x = end_x
        
        # Switch color
        current_color = color2 if current_color == color1 else color1
        
        # Draw vertical part of zigzag
        if (x, y) != (x2, y2):
            end_y = min(y2, max(y1, y + dy * step_size)) if dy > 0 else max(y2, min(y1, y + dy * step_size))
            draw_line(output_grid, x, y, length=abs(end_y - y), color=current_color, direction=(0, dy))
            y = end_y
        
        # Switch color
        current_color = color2 if current_color == color1 else color1
    
    return output_grid

def generate_input():
    # Create a black grid
    n = m = np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Choose two different colors
    colors = np.random.choice(list(Color.NOT_BLACK), size=2, replace=False)
    
    # Place two colored pixels
    positions = np.random.choice(n*m, size=2, replace=False)
    grid[positions // m, positions % m] = colors
    
    return grid