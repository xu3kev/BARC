from common import *

import numpy as np
from typing import *

# concepts:
# repetition, symmetry, horizontal/vertical bars, collision detection

# description:
# In the input, you will see two colored pixels on opposite edges of the grid.
# Create bars by extending these pixels to the opposite edge, then repeat these bars
# in both directions (up/down for vertical bars, left/right for horizontal bars).
# When the bars intersect, create a small square of the mixed color at the intersection.
# Continue this pattern until the entire grid is filled.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the two colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    assert len(colored_pixels) == 2, "Input should have exactly two colored pixels"

    pixel1, pixel2 = colored_pixels
    x1, y1 = pixel1
    x2, y2 = pixel2
    color1, color2 = input_grid[x1, y1], input_grid[x2, y2]

    output_grid = np.full_like(input_grid, Color.BLACK)

    # Determine if bars are horizontal or vertical
    if (x1 == 0 or x1 == input_grid.shape[0] - 1) and (x2 == 0 or x2 == input_grid.shape[0] - 1):
        # Vertical bars
        bar_width = abs(y2 - y1)
        for i in range(0, input_grid.shape[1], bar_width):
            output_grid[:, i:i+bar_width//2] = color1
            output_grid[:, i+bar_width//2:i+bar_width] = color2
    else:
        # Horizontal bars
        bar_height = abs(x2 - x1)
        for i in range(0, input_grid.shape[0], bar_height):
            output_grid[i:i+bar_height//2, :] = color1
            output_grid[i+bar_height//2:i+bar_height, :] = color2

    # Create mixed color squares at intersections
    mixed_color = mix_colors(color1, color2)
    for x in range(1, output_grid.shape[0] - 1):
        for y in range(1, output_grid.shape[1] - 1):
            if (output_grid[x-1, y] != output_grid[x+1, y] and 
                output_grid[x, y-1] != output_grid[x, y+1]):
                output_grid[x-1:x+2, y-1:y+2] = mixed_color

    return output_grid

def mix_colors(color1, color2):
    # Simple color mixing function
    if color1 == Color.RED and color2 == Color.BLUE or color2 == Color.RED and color1 == Color.BLUE:
        return Color.PURPLE
    elif color1 == Color.RED and color2 == Color.YELLOW or color2 == Color.RED and color1 == Color.YELLOW:
        return Color.ORANGE
    elif color1 == Color.BLUE and color2 == Color.YELLOW or color2 == Color.BLUE and color1 == Color.YELLOW:
        return Color.GREEN
    else:
        return Color.GREY  # Default mixed color

def generate_input() -> np.ndarray:
    # Create a grid with random dimensions
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    # Decide if bars will be horizontal or vertical
    is_vertical = np.random.choice([True, False])

    if is_vertical:
        # Place two colored pixels on top and bottom edges
        y1, y2 = np.random.choice(range(m), size=2, replace=False)
        grid[0, y1] = np.random.choice([Color.RED, Color.BLUE, Color.YELLOW])
        grid[-1, y2] = np.random.choice([Color.RED, Color.BLUE, Color.YELLOW])
    else:
        # Place two colored pixels on left and right edges
        x1, x2 = np.random.choice(range(n), size=2, replace=False)
        grid[x1, 0] = np.random.choice([Color.RED, Color.BLUE, Color.YELLOW])
        grid[x2, -1] = np.random.choice([Color.RED, Color.BLUE, Color.YELLOW])

    return grid