import numpy as np
from typing import *
from common import *

# concepts:
# patterns, counting, incrementing, state-based grid evolution

# description:
# In the input grid, cells have different colors. A cell's new state is determined by the majority color of its neighbors in the 8 surrounding cells (Moore neighborhood).
# If multiple colors equally share the majority, the cell retains its previous state.

def main(input_grid: np.ndarray) -> np.ndarray:
    def majority_color(neighbors):
        if len(neighbors) == 0:
            return Color.BLACK
        colors, counts = np.unique(neighbors, return_counts=True)
        max_count = np.max(counts)
        max_colors = colors[counts == max_count]
        if len(max_colors) > 1:
            return None
        return max_colors[0]

    rows, cols = input_grid.shape
    output_grid = input_grid.copy()
    for i in range(rows):
        for j in range(cols):
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors.append(input_grid[ni, nj])
            new_color = majority_color(neighbors)
            if new_color:
                output_grid[i, j] = new_color
    return output_grid

def generate_input() -> np.ndarray:
    rows, cols = np.random.randint(10, 16, size=2)
    grid = np.random.choice(list(Color.ALL_COLORS), size=(rows, cols))
    return grid