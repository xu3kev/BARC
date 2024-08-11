from common import *

import numpy as np
import random
from typing import *

# concepts:
# symmetry detection, patterns, horizontal bars

# description:
# In the input grid, you will see a colored pattern that is symmetric around the vertical midline.
# To produce the output grid, identify the vertical symmetry axis, and replace all pixels that are along that axis with a horizontal bar of grey pixels.
# Extend this grey bar horizontally, and maintain symmetry throughout the grid.

def main(input_grid):
    # Detect vertical symmetry axis
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[])
    assert len(symmetries) > 0, "No translational symmetry found"

    n, m = input_grid.shape
    output_grid = np.copy(input_grid)

    # Calculate the vertical midline
    midline = m // 2

    # Draw the grey bar along the midline
    draw_line(output_grid, midline, 0, length=n, color=Color.GREY, direction=(0, 1))

    # Expand the symmetry to maintain the pattern
    for x, y in np.argwhere(input_grid != Color.BLACK):
        if y < midline:
            symmetric_y = m - y - 1
            output_grid[x, symmetric_y] = input_grid[x, y]
        elif y > midline:
            symmetric_y = m - y - 1
            output_grid[x, symmetric_y] = input_grid[x, y]

    return output_grid


def generate_input():
    # Create a (20, 20) grid
    n, m = 20, 20
    input_grid = np.full((n, m), Color.BLACK)

    # Choose a pattern color
    pattern_color = random.choice(Color.NOT_BLACK)

    # Create a random pattern with vertical symmetry
    for x in range(n):
        for y in range(m // 2):
            if random.random() < 0.4:  # Fill about 40% of the grid with the pattern color
                input_grid[x, y] = pattern_color
                input_grid[x, m - y - 1] = pattern_color

    return input_grid