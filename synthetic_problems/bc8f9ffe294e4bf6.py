from common import *

import numpy as np
from typing import *

# concepts:
# color, lines, collision detection

# description:
# In the input you will see a red pixel and a teal pixel.
# To create the output:
# 1. Draw a blue diagonal line from the red pixel to the teal pixel.
# 2. Draw green lines from the red and teal pixels to the edges of the grid, but stop if they intersect the blue diagonal line.

def main(input_grid: np.ndarray) -> np.ndarray:
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the red and teal pixels
    red_x, red_y = np.where(input_grid == Color.RED)
    teal_x, teal_y = np.where(input_grid == Color.TEAL)
    
    # Draw the blue diagonal line from the red pixel to the teal pixel
    dx = np.sign(teal_x - red_x)[0]
    dy = np.sign(teal_y - red_y)[0]
    draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.BLUE, direction=(dx, dy), stop_at_color=[Color.TEAL])

    # Draw green lines extending from the red pixel
    # Line to the left edge
    draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.GREEN, direction=(0, -1), stop_at_color=[Color.BLUE])
    # Line to the right edge
    draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.GREEN, direction=(0, 1), stop_at_color=[Color.BLUE])
    # Line to the top edge
    draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.GREEN, direction=(-1, 0), stop_at_color=[Color.BLUE])
    # Line to the bottom edge
    draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.GREEN, direction=(1, 0), stop_at_color=[Color.BLUE])

    # Draw green lines extending from the teal pixel
    # Line to the left edge
    draw_line(output_grid, teal_x[0], teal_y[0], length=None, color=Color.GREEN, direction=(0, -1), stop_at_color=[Color.BLUE])
    # Line to the right edge
    draw_line(output_grid, teal_x[0], teal_y[0], length=None, color=Color.GREEN, direction=(0, 1), stop_at_color=[Color.BLUE])
    # Line to the top edge
    draw_line(output_grid, teal_x[0], teal_y[0], length=None, color=Color.GREEN, direction=(-1, 0), stop_at_color=[Color.BLUE])
    # Line to the bottom edge
    draw_line(output_grid, teal_x[0], teal_y[0], length=None, color=Color.GREEN, direction=(1, 0), stop_at_color=[Color.BLUE])

    return output_grid


def generate_input() -> np.ndarray:
    # make a black grid as the background
    n = np.random.randint(6, 15)
    m = np.random.randint(6, 15)
    grid = np.zeros((n, m), dtype=int)

    # select a random position for the red pixel
    red_x = np.random.randint(0, n)
    red_y = np.random.randint(0, m)
    grid[red_x, red_y] = Color.RED

    # select a random position for the teal pixel
    teal_x = np.random.randint(0, n)
    teal_y = np.random.randint(0, m)
    grid[teal_x, teal_y] = Color.TEAL

    # check if the red and teal pixels are in the same row or column
    # if they are, then try again
    if red_x == teal_x or red_y == teal_y:
        return generate_input()
    
    return grid