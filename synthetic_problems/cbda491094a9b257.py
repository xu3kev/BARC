from common import *

import numpy as np
from typing import *

# concepts:
# lines, patterns, pixel manipulation

# description:
# In the input, you will see a grid of black background with a diagonal green line and potentially some other colored pixels.
# To make the output, extend the green line to the edges of the grid or other green pixels. Then, for each non-green, non-black pixel, draw lines in the diagonal directions (northeast, northwest, southeast, southwest) until they hit the edge of the grid or other colored pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    # Extend the green line to the edges or other green pixels
    green_line_coords = np.argwhere(input_grid == Color.GREEN)

    if len(green_line_coords) > 0:
        x1, y1 = np.min(green_line_coords, axis=0)
        x2, y2 = np.max(green_line_coords, axis=0)

        draw_line(output_grid, x1, y1, length=None, color=Color.GREEN, direction=(-1, -1), stop_at_color=[Color.GREEN])
        draw_line(output_grid, x2, y2, length=None, color=Color.GREEN, direction=(1, 1), stop_at_color=[Color.GREEN])

    # For each non-green, non-black pixel, draw diagonal lines until hitting the edge or another colored pixel
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x, y]
            if color != Color.BLACK and color != Color.GREEN:
                draw_line(output_grid, x, y, length=None, color=color, direction=(-1, -1), stop_at_color=[Color.BLACK, Color.GREEN])
                draw_line(output_grid, x, y, length=None, color=color, direction=(1, 1), stop_at_color=[Color.BLACK, Color.GREEN])
                draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 1), stop_at_color=[Color.BLACK, Color.GREEN])
                draw_line(output_grid, x, y, length=None, color=color, direction=(1, -1), stop_at_color=[Color.BLACK, Color.GREEN])

    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK, dtype=int)
    
    # Create a diagonal green line
    length = np.random.randint(3, min(n, m) - 2)
    start_x, start_y = np.random.randint(1, n-length), np.random.randint(1, m-length)
    draw_line(grid, start_x, start_y, length=length, color=Color.GREEN, direction=(1, 1))
    
    # Scatter some non-green, non-black pixels
    num_other_pixels = np.random.randint(5, 10)
    for _ in range(num_other_pixels):
        while True:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = np.random.choice([color for color in Color.NOT_BLACK if color != Color.GREEN])
                break
                
    return grid