from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, collision detection, pixel manipulation

# description:
# In the input, you will see a vertical grey line on a black background, with red and blue pixels scattered on either side of the line.
# To make the output, draw horizontal lines from each of the red and blue pixels towards the grey line.
# The lines from red pixels should stop when they hit the grey line or a blue pixel's line.
# The lines from blue pixels should stop when they hit the grey line or a red pixel's line.
# If a red line and a blue line collide, they both stop at the point of collision.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find the location of the vertical grey line
    grey_line = np.where(output_grid == Color.GREY)
    grey_line_x = np.unique(grey_line[1])[0]
    
    # Find the red and blue pixels
    red_pixels = np.argwhere(output_grid == Color.RED)
    blue_pixels = np.argwhere(output_grid == Color.BLUE)
    
    # Sort pixels by distance to grey line (furthest first)
    red_pixels = sorted(red_pixels, key=lambda p: abs(p[1] - grey_line_x), reverse=True)
    blue_pixels = sorted(blue_pixels, key=lambda p: abs(p[1] - grey_line_x), reverse=True)
    
    # Draw lines from red pixels
    for x, y in red_pixels:
        direction = 1 if y < grey_line_x else -1
        draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, direction), 
                  stop_at_color=[Color.GREY, Color.BLUE])
    
    # Draw lines from blue pixels
    for x, y in blue_pixels:
        direction = 1 if y < grey_line_x else -1
        draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, direction), 
                  stop_at_color=[Color.GREY, Color.RED])
    
    return output_grid

def generate_input():
    n, m = 20, 20
    grid = np.zeros((n, m), dtype=int)
    
    # Create vertical grey line
    col = np.random.randint(m // 3, 2 * (m // 3))
    grid[:, col] = Color.GREY
    
    # Place red and blue pixels
    for _ in range(np.random.randint(5, 10)):
        x = np.random.randint(n)
        y = np.random.randint(col) if np.random.random() < 0.5 else np.random.randint(col + 1, m)
        color = Color.RED if np.random.random() < 0.5 else Color.BLUE
        if grid[x, y] == Color.BLACK:
            grid[x, y] = color
    
    return grid