from common import *

import numpy as np
from typing import *

# concepts:
# repetition, horizontal/vertical bars, flood fill, connecting same color

# description:
# In the input, you will see two colored pixels on opposite edges of the grid.
# For each pixel, create a bar (horizontal or vertical depending on its position) that extends to the opposite side.
# Then, flood fill the area between these two bars with the color of the bar closer to that area.
# Finally, repeat this pattern vertically and horizontally to fill the entire grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the two colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    assert len(colored_pixels) == 2, "Input should have exactly two colored pixels"

    # Extract positions and colors
    (x1, y1), (x2, y2) = colored_pixels
    color1, color2 = input_grid[x1, y1], input_grid[x2, y2]

    # Create output grid
    output_grid = np.zeros_like(input_grid)
    
    # Determine if bars are horizontal or vertical
    if x1 in (0, input_grid.shape[0] - 1) and x2 in (0, input_grid.shape[0] - 1):
        # Horizontal bars
        output_grid[x1, :] = color1
        output_grid[x2, :] = color2
        # Flood fill between bars
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            output_grid[x, :] = color1 if abs(x - x1) < abs(x - x2) else color2
    else:
        # Vertical bars
        output_grid[:, y1] = color1
        output_grid[:, y2] = color2
        # Flood fill between bars
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            output_grid[:, y] = color1 if abs(y - y1) < abs(y - y2) else color2

    # Repeat the pattern
    pattern = output_grid.copy()
    h, w = pattern.shape
    output_grid = np.tile(pattern, (3, 3))[:h, :w]

    return output_grid

def generate_input() -> np.ndarray:
    # Create a grid of random size between 10x10 and 20x20
    size = np.random.randint(10, 21)
    grid = np.zeros((size, size), dtype=int)

    # Choose two different colors
    colors = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)

    # Decide between horizontal or vertical bars
    if np.random.choice([True, False]):
        # Horizontal bars
        x1, x2 = 0, size - 1
        y1, y2 = np.random.randint(0, size, 2)
    else:
        # Vertical bars
        y1, y2 = 0, size - 1
        x1, x2 = np.random.randint(0, size, 2)

    # Place the colored pixels
    grid[x1, y1] = colors[0]
    grid[x2, y2] = colors[1]

    return grid