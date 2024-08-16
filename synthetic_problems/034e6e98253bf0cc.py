from common import *
import numpy as np
from typing import *

def main(input_grid):
    # Copy the input grid to the output grid
    output_grid = np.copy(input_grid)
    
    # Find the location of the horizontal grey line
    grey_line = np.where(output_grid == Color.GREY)
    grey_line_y = np.unique(grey_line[1])
    
    # Find the red and blue pixels
    red_pixels = np.where(output_grid == Color.RED)
    blue_pixels = np.where(output_grid == Color.BLUE)
    
    # Draw diagonal lines from the red pixels towards the grey line
    for i in range(len(red_pixels[0])):
        x, y = red_pixels[0][i], red_pixels[1][i]
        # Draw lines diagonally toward the grey line
        if y < grey_line_y:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(1, 1))
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(-1, 1))
        else:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(1, -1))
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(-1, -1))

    # Draw diagonal lines from the blue pixels away from the grey line
    for i in range(len(blue_pixels[0])):
        x, y = blue_pixels[0][i], blue_pixels[1][i]
        # Draw lines diagonally away from the grey line
        if y < grey_line_y:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(1, -1))
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(-1, -1))
        else:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(1, 1))
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(-1, 1))
            
    return output_grid

def generate_input():
    # Create a 10x10 black grid for the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # Create a horizontal grey line on a random row around halfway down the grid
    row = np.random.randint(m // 3, 2 * (m // 3))
    grid[:, row] = Color.GREY
    
    # Scatter a random number of red and blue pixels on either side of the grey line
    # Select columns for pixels above the grey line
    cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
    for col in cols:
        if np.random.rand() < 0.5:
            grid[np.random.randint(row), col] = Color.RED
        else:
            grid[np.random.randint(row), col] = Color.BLUE
            
    # Select columns for pixels below the grey line
    cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
    for col in cols:
        if np.random.rand() < 0.5:
            grid[np.random.randint(row + 1, m), col] = Color.RED
        else:
            grid[np.random.randint(row + 1, m), col] = Color.BLUE
    
    return grid