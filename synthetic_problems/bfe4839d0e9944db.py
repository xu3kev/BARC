from common import *

import numpy as np
from typing import *

# concepts:
# objects, repeating pattern, connecting colors

# description:
# In the input grid, there will be a single color creating a series of equally spaced horizontal lines. These lines will be dotted, meaning there will be gaps between the colored cells. 
# The puzzle requires connecting these dots to create continuous lines. Once the lines are completed, we will repeat the pattern downwards to fill the entire grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    def fill_lines(grid, start_points, color):
        """
        Connects dots in horizontal lines
        """
        for y, xs in start_points.items():
            if len(xs) > 1:
                for i in range(len(xs) - 1):
                    draw_line(grid, xs[i], y, xs[i+1] - xs[i], color, direction=(1, 0))
        
    # Create output grid
    output_grid = input_grid.copy()

    # Find the colored dots and categorize by rows
    rows_with_dots = {}
    for y in range(input_grid.shape[1]):
        row = np.where(input_grid[y] != Color.BLACK)[0]
        if row.size > 0:
            rows_with_dots[y] = row

    # Get the color of the dots
    dot_color = input_grid[rows_with_dots[list(rows_with_dots.keys())[0]][0], list(rows_with_dots.keys())[0]]

    # Fill lines
    fill_lines(output_grid, rows_with_dots, dot_color)
    
    # Repeat the pattern
    rows = sorted(rows_with_dots.keys())
    if len(rows) > 1:
        pattern_height = rows[1] - rows[0]
        for i in range(1, input_grid.shape[0] // pattern_height):
            for r in rows:
                output_grid[(r + i*pattern_height) % input_grid.shape[0]] = output_grid[r]

    return output_grid

def generate_input() -> np.ndarray:
    # Create a 20x20 black grid
    input_grid = np.full((20, 20), Color.BLACK)

    # Choose a color for the lines
    line_color = np.random.choice(Color.NOT_BLACK)

    # Create dotted horizontal lines
    num_lines = np.random.randint(2, 5)  # 2 to 4 lines
    for _ in range(num_lines):
        y = np.random.randint(0, 20)
        x_positions = sorted(np.random.choice(range(20), np.random.randint(4, 8), replace=False))
        for x in x_positions:
            input_grid[y, x] = line_color

    return input_grid