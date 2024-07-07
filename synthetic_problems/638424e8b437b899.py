from common import *

import numpy as np
from typing import *

# concepts:
# colors
# neighbor analysis

# description:
# In the input grid, each pixel color is updated to the most frequent color of its cardinal neighbors (top, bottom, left, and right).
# If there are multiple colors with the same frequency, the pixel keeps its original color.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    for x in range(rows):
        for y in range(cols):
            neighbors = []
            if x > 0:
                neighbors.append(input_grid[x-1, y])
            if x < rows - 1:
                neighbors.append(input_grid[x+1, y])
            if y > 0:
                neighbors.append(input_grid[x, y-1])
            if y < cols - 1:
                neighbors.append(input_grid[x, y+1])
            
            if neighbors:
                color_counts = {}
                for color in neighbors:
                    if color in color_counts:
                        color_counts[color] += 1
                    else:
                        color_counts[color] = 1
                most_frequent_color = max(color_counts, key=color_counts.get)
                # Check if there's a tie
                if list(color_counts.values()).count(color_counts[most_frequent_color]) == 1:
                    output_grid[x, y] = most_frequent_color
    return output_grid


def generate_input() -> np.ndarray:
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    input_grid = np.random.choice(list(Color.NOT_BLACK), size=(n, m))
    return input_grid