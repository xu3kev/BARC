from common import *

import numpy as np
from typing import *

# concepts:
# patterns, color mapping, reflection

# description:
# In the input grid, there will be patterns of vertical stripes of various colors. Some stripes might be reflected horizontally or vertically.
# To create the output, first identify the base stripe pattern without any reflections. Then, apply a color mapping to the identified base pattern.

def main(input_grid):
    # Get the size of the input grid
    n, m = input_grid.shape

    # Find the period of the vertical stripes
    for period in range(1, m):
        base_pattern = input_grid[:, :period]
        repetitions = [input_grid[:, i*period:(i+1)*period] for i in range(m // period)]

        # Check if every repetition matches the base pattern or its reflections
        is_valid = all(any(np.array_equal(rep, np.flip(base_pattern, axis)) for rep in repetitions for axis in [None, 0, 1]) for rep in repetitions)
        
        if is_valid:
            break

    # Apply the color mapping to the base pattern
    output_grid = input_grid.copy()
    output_grid = np.vectorize(lambda color: color_map.get(color, color))(output_grid)
    
    return output_grid


color_map = {
    Color.GREEN: Color.YELLOW,
    Color.BLUE: Color.GRAY,
    Color.RED: Color.PINK,
    Color.TEAL: Color.MAROON,
    Color.YELLOW: Color.GREEN,
    Color.GRAY: Color.BLUE,
    Color.PINK: Color.RED,
    Color.MAROON: Color.TEAL
}


def generate_input():
    # Create random stripe pattern, ensuring vertical stripes and possible reflections
    height = np.random.randint(5, 10)
    width = np.random.randint(5, 10)
    period = np.random.randint(2, (width // 2) + 1)
    base_pattern = np.zeros((height, period), dtype=int)
    
    for col in range(period):
        color = np.random.choice(list(color_map.keys()))
        base_pattern[:, col] = color
    
    grid = np.tile(base_pattern, (1, width // period + 1))[:, :width]
    
    # Apply random reflections
    if np.random.rand() < 0.5:
        grid = np.flip(grid, axis=0)  # Horizontal reflection
    if np.random.rand() < 0.5:
        grid = np.flip(grid, axis=1)  # Vertical reflection

    return grid