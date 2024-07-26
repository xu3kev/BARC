from common import *

import numpy as np

# concepts:
# Sliding objects, shapes, repetition, alignment

# description:
# In the input, we will have a grid with one or more horizontal bars of various sizes and colors placed at different vertical heights.
# To create the output grid, we will slide each of the horizontal bars downwards until they all lie at the bottommost row of the grid, without overlapping each other.
# If any bars overlap in this process, the one encountered first (going from top to bottom in the input grid) will be placed at the bottommost available position for it.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Making a copy of input grid to create the output grid
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Collect bars with their color and initial positions
    bars_info = []
    m, n = input_grid.shape
    for y in range(n):
        x_start = None
        for x in range(m):
            if input_grid[x, y] != Color.BLACK:
                if x_start is None:
                    x_start = x
                if x == m-1 or input_grid[x+1, y] == Color.BLACK:
                    bars_info.append((x_start, x, y, input_grid[x, y]))
                    x_start = None

    # Sort bars first by color, then by positions
    bars_info.sort(key=lambda x: x[2])

    # Place bars at the bottom to top
    current_bottom_row = m - 1
    for bar_info in bars_info:
        _start, _end, col, color = bar_info
        while True:
            if not any(output_grid[row][_start:_end+1] != Color.BLACK for row in range(current_bottom_row, current_bottom_row+1)):
                output_grid[current_bottom_row][_start:_end+1] = [color] * (_end - _start + 1)
                current_bottom_row = min(current_bottom_row - 1, 0)
                break
            else:
                current_bottom_row -= 1

    return output_grid

def generate_input() -> np.ndarray:
    # Create a black grid of size WxH, and place random horizontal bars
    W, H = 10, np.random.randint(10, 21)
    input_grid = np.zeros((H, W), dtype=int)

    # Random number of bars to place
    num_bars = np.random.randint(1, 6)

    # Place bars randomly
    for _ in range(num_bars):
        bar_length = np.random.randint(2, W - 1)
        bar_color = np.random.choice(list(Color.NOT_BLACK))
        x_start = np.random.randint(0, W - bar_length + 1)
        y_pos = np.random.randint(0, H)

        while any(input_grid[y_pos, x_start:x_start + bar_length] != Color.BLACK):
            y_pos = (y_pos + 1) % H

        input_grid[y_pos, x_start:x_start + bar_length] = bar_color

    return input_grid