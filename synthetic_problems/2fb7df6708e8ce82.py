from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, pixel manipulation

# description:
# In the input grid, there is a horizontal grey line dividing the grid into two parts. There are randomly placed red and blue pixels placed above and below the grey line
# respectivley. The task is to transform the grid by adding 'force field' lines: For each red pixel, attach a vertical line going upwards to the top edge, stopping only if a 'magnet' is encountered.
# The lines should be of the same color as the red pixels. For each blue pixel, attach a vertical line going downwards to the bottom edge, stopping only if a 'magnet' is encountered.
# The lines should be of the same color as the blue pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    grey_line = np.where(output_grid == Color.GREY)
    if len(grey_line[0]) == 0:
        return output_grid    # safeguard for no grey line present.
    
    grey_line_y = np.unique(grey_line[1])[0]
    
    red_pixels = np.where(output_grid == Color.RED)
    blue_pixels = np.where(output_grid == Color.BLUE)
    magnet_pixels = np.where(output_grid == Color.GREEN)
    
    # draw lines from the red pixels upwards, stopping at 'magnet' pixels
    for i in range(len(red_pixels[0])):
        x, y = red_pixels[0][i], red_pixels[1][i]
        draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, -1), stop_at_color=[Color.GREEN])

    # draw lines from the blue pixels downwards
    for i in range(len(blue_pixels[0])):
        x, y = blue_pixels[0][i], blue_pixels[1][i]
        draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, 1), stop_at_color=[Color.GREEN])

    return output_grid


def generate_input() -> np.ndarray:
    n = m = 10
    grid = np.zeros((n,m), dtype=int)
    
    row = np.random.randint(m//3, 2*(m//3))
    grid[:, row] = Color.GREY
    
    # scatter red and blue pixels, ensuring no column has both a red and blue pixel
    red_cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
    blue_cols = np.random.choice(np.arange(m), size=np.random.randint(3,7), replace=False)
    
    while len(set(red_cols) & set(blue_cols)) > 0:
        red_cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
        blue_cols = np.random.choice(np.arange(m), size=np.random.randint(3,7), replace=False)
    
    for col in red_cols:
        x_red = np.random.randint(0, row)
        grid[col, x_red] = Color.RED
    
    for col in blue_cols:
        x_blue = np.random.randint(row+1, m)
        grid[col, x_blue] = Color.BLUE
    
    # scatter magnet pixels above or below red and blue pixels
    num_magnets = np.random.randint(2, 6)
    for _ in range(num_magnets):
        if np.random.rand() < 0.5:
            x_magnet = np.random.randint(0, row)
            y_magnet = np.random.randint(0, m)
        else:
            x_magnet = np.random.randint(row+1, m)
            y_magnet = np.random.randint(0, m)
        grid[y_magnet, x_magnet] = Color.GREEN
    
    return grid