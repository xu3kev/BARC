from common import *

import numpy as np
from typing import *

# concepts:
# patterns, horizontal/vertical bars, color guides

# description:
# In the input you will see a grid with a pattern composed of colored horizontal and vertical bars. There will be a single special pixel with a unique color that is not used in the bars.
# To make the output, extend lines from the special pixel to all horizontal and vertical bars. For each bar the line intersects, copy the color from the special pixel to the point of intersection with that bar.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # get the index of the special pixel
    all_colors, counts = np.unique(input_grid, return_counts=True)
    special_color = all_colors[np.argmax(counts == 1)]
    special_pixel = np.where(input_grid == special_color)
    x, y = special_pixel[0][0], special_pixel[1][0]

    # find the horizontal and vertical bars
    horizontal_bars = np.where(np.all(input_grid != Color.BLACK, axis=1))[0]
    vertical_bars = np.where(np.all(input_grid != Color.BLACK, axis=0))[0]

    # extend lines from the special pixel to all horizontal bars
    for hb in horizontal_bars:
        output_grid[hb, y] = special_color

    # extend lines from the special pixel to all vertical bars
    for vb in vertical_bars:
        output_grid[x, vb] = special_color

    return output_grid


def generate_input():
    n = m = 10  # Grid size
    grid = np.zeros((n, m), dtype=int)
    
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)

    # add horizontal bars
    for i in range(np.random.randint(2, 4)):
        row = np.random.randint(0, n)
        color = colors.pop()
        grid[row, :] = color
    
    # add vertical bars
    for j in range(np.random.randint(2, 4)):
        col = np.random.randint(0, m)
        color = colors.pop()
        grid[:, col] = color

    # add a special pixel that is not in the bars
    while True:
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        if grid[x, y] == 0:  # Ensure it's in the black (background) area
            break

    special_color = colors.pop()
    grid[x, y] = special_color

    return grid