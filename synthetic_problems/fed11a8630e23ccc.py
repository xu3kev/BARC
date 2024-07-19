from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation, repeating patterns, connecting colors

# description:
# In the input grid, you will see a pair of horizontally or vertically aligned colored pixels. 
# To create the output grid, draw a line joining the two pixels and repeat this line spacing it evenly till the edges 
# of the grid in the direction perpendicular to the initial alignment.

def main(input_grid: np.ndarray) -> np.ndarray:
    # find the individual coloured pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)

    # there should be exactly two colored pixels
    assert len(colored_pixels) == 2

    # find the two pixels
    pixel1, pixel2 = colored_pixels
    x1, y1 = pixel1
    x2, y2 = pixel2
    color1, color2 = input_grid[x1, y1], input_grid[x2, y2]

    # make the line between the two points
    output_grid = np.copy(input_grid)

    # check if they are horizontally or vertically aligned and connect them accordingly
    if x1 == x2:
        # horizontally aligned
        for y in range(min(y1, y2), max(y1, y2) + 1):
            output_grid[x1, y] = color1
        # calculate the step size for repeating the pattern
        step_size = abs(y2 - y1) + 1
        for i in range(1, (output_grid.shape[0] - x1) // step_size):
            if x1 + step_size * i < output_grid.shape[0]:
                output_grid[x1 + step_size * i, min(y1, y2):max(y1, y2) + 1] = color1
            if x1 - step_size * i >= 0:
                output_grid[x1 - step_size * i, min(y1, y2):max(y1, y2) + 1] = color1
    elif y1 == y2:
        # vertically aligned
        for x in range(min(x1, x2), max(x1, x2) + 1):
            output_grid[x, y1] = color1
        # calculate the step size for repeating the pattern
        step_size = abs(x2 - x1) + 1
        for i in range(1, (output_grid.shape[1] - y1) // step_size):
            if y1 + step_size * i < output_grid.shape[1]:
                output_grid[min(x1, x2):max(x1, x2) + 1, y1 + step_size * i] = color1
            if y1 - step_size * i >= 0:
                output_grid[min(x1, x2):max(x1, x2) + 1, y1 - step_size * i] = color1

    return output_grid


def generate_input() -> np.ndarray:
    # make a grid that is narrow and tall. 
    n = np.random.randint(5, 10)
    m = np.random.randint(n+1, 30)
    grid = np.zeros((n, m), dtype=int)

    # place two colored pixels. 
    if np.random.choice([True, False]):
        # horizontally aligned
        x = np.random.randint(n)
        y1 = np.random.randint(m - 1)
        y2 = np.random.randint(y1 + 1, m)
        color1, color2 = random.sample(Color.NOT_BLACK, 2)
        grid[x, y1] = color1
        grid[x, y2] = color2
    else:
        # vertically aligned
        y = np.random.randint(m)
        x1 = np.random.randint(n - 1)
        x2 = np.random.randint(x1 + 1, n)
        color1, color2 = random.sample(Color.NOT_BLACK, 2)
        grid[x1, y] = color1
        grid[x2, y] = color2

    return grid