from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, objects, alignment

# description:
# In the input you will see three colored pixels: red, blue, and yellow. These pixels form a triangle.
# To make the output, draw lines connecting these pixels to form the triangle. The color of each line should be the mixture of the two colors it's connecting:
# Red + Blue = Purple
# Blue + Yellow = Green
# Red + Yellow = Orange
# The lines should be drawn using the shortest path (horizontal then vertical, or vertical then horizontal).

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find the positions of the colored pixels
    red_pos = np.argwhere(input_grid == Color.RED)[0]
    blue_pos = np.argwhere(input_grid == Color.BLUE)[0]
    yellow_pos = np.argwhere(input_grid == Color.YELLOW)[0]
    
    # Define color mixtures
    color_mix = {
        frozenset([Color.RED, Color.BLUE]): Color.PINK,
        frozenset([Color.BLUE, Color.YELLOW]): Color.GREEN,
        frozenset([Color.RED, Color.YELLOW]): Color.ORANGE
    }
    
    # Draw lines between the points
    for start, end, colors in [(red_pos, blue_pos, frozenset([Color.RED, Color.BLUE])),
                               (blue_pos, yellow_pos, frozenset([Color.BLUE, Color.YELLOW])),
                               (red_pos, yellow_pos, frozenset([Color.RED, Color.YELLOW]))]:
        # Draw horizontal line
        draw_line(output_grid, start[0], start[1], length=abs(end[1]-start[1]), 
                  color=color_mix[colors], direction=(0, 1 if end[1] > start[1] else -1))
        
        # Draw vertical line
        draw_line(output_grid, start[0], end[1], length=abs(end[0]-start[0]), 
                  color=color_mix[colors], direction=(1 if end[0] > start[0] else -1, 0))
    
    return output_grid

def generate_input():
    # Create a black grid
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Place three colored pixels
    colors = [Color.RED, Color.BLUE, Color.YELLOW]
    for color in colors:
        while True:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                break
    
    return grid