from common import *

import numpy as np
from typing import *

# concepts:
# proximity, color change, horizontal/vertical bars

# description:
# In the input you will see a pair of lines on the edge of the canvas that are either horizontal or vertical, and also green pixels randomly placed in between the lines
# Change the color of each green pixel to match the color of the line it is closest to

def main(input_grid: np.ndarray) -> np.ndarray:
    # find the two lines by removing the green pixels
    lines = np.copy(input_grid)
    lines[input_grid == Color.GREEN] = Color.BLACK

    # lines now contains only the lines, which are going to be used to assign color to the green pixels
    output_grid = np.copy(input_grid)

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] == Color.GREEN:
                # find the closest point on the lines
                closest_x, closest_y = min([(i, j) for i in range(input_grid.shape[0]) for j in range(input_grid.shape[1]) if lines[i, j] != Color.BLACK],
                                           key=lambda p: abs(p[0] - x) + abs(p[1] - y))
                color_of_closest_line = lines[closest_x, closest_y]
                output_grid[x, y] = color_of_closest_line
    
    return output_grid

def generate_input() -> np.ndarray:
    # make a black grid first as background
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # sprinkle green pixels randomly
    for green_index in range(random.randint(5, 20)):
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
        grid[x, y] = Color.GREEN

    # decide on a pair of colors for the horizontal/vertical lines
    line_colors = random.sample([color for color in Color.ALL_COLORS if color != Color.GREEN and color != Color.BLACK], 2)

    # flip a coin to decide whether it is horizontal or vertical
    is_horizontal = random.choice([True, False])
    if is_horizontal:
        grid[:, 0] = line_colors[0]
        grid[:, -1] = line_colors[1]
    else:
        grid[0, :] = line_colors[0]
        grid[-1, :] = line_colors[1]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)