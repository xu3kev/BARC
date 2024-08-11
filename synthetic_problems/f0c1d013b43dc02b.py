from common import *
import numpy as np
from typing import *

# concepts:
# rectangular cells, topology, counting

# description:
# The input grid contains 2x2 cells of various colors scattered within the grid. Additionally, there are individually colored pixels.
# The goal is to count the number of each 2x2 colored cell in the input.
# The output will be a vertical bar for each distinct color with a length proportional to the count of that 2x2 colored cell multiplies by 2 (each 2x2 cell counts as 2 pixels in length).

def main(input_grid: np.ndarray) -> np.ndarray:
    # Count each 2x2 colored cell
    color_counts = {}
    for x in range(input_grid.shape[0] - 1):
        for y in range(input_grid.shape[1] - 1):
            cell = input_grid[x:x+2, y:y+2]
            unique_colors = np.unique(cell)
            if len(unique_colors) == 1 and unique_colors[0] != Color.BLACK:
                color = unique_colors[0]
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1

    # Determine the output grid size, based on the number of unique colors and their counts
    unique_colors = list(color_counts.keys())
    max_count = max(color_counts.values(), default=0)
    output_grid_height = max_count * 2
    output_grid_width = len(unique_colors)

    # Initialize the output grid
    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)

    # Fill the vertical bars corresponding to each color
    for col_index, color in enumerate(unique_colors):
        for row_index in range(color_counts[color] * 2):
            output_grid[output_grid_height - 1 - row_index, col_index] = color

    return output_grid


def generate_input() -> np.ndarray:
    # Create a grid size between 10x10 to 20x20
    n = np.random.randint(10, 21)
    grid = np.zeros((n, n), dtype=int)

    # Randomly decide the colors to be used
    colors = random.sample(Color.NOT_BLACK, np.random.randint(2, 5))

    # Fill the grid with 2x2 colored cells
    for _ in range(np.random.randint(5, 15)):
        color = random.choice(colors)
        x, y = random_free_location_for_sprite(grid, np.full((2, 2), color))
        blit_sprite(grid, np.full((2, 2), color), x, y)

    # Add some individually colored pixels
    for _ in range(np.random.randint(10, 30)):
        color = random.choice(colors)
        x, y = random_free_location_for_sprite(grid, np.full((1, 1), color))
        blit_sprite(grid, np.full((1, 1), color), x, y)
    
    return grid