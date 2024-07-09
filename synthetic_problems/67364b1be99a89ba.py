from common import *
import numpy as np
from typing import *

# concepts:
# symmetry detection, coloring based on adjacency, objects

# description:
# The input grid consists of various shapes, each colored uniquely.
# Detect horizontal symmetry; only consider objects with horizontal symmetry.
# For each symmetric object, color all adjacent pixels of these objects with a new specific color.

def main(input_grid):
    output_grid = np.copy(input_grid)
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=True)

    for obj in objects:
        if detect_horizontal_symmetry(obj):
            highlight_adjacent(output_grid, obj)

    return output_grid

def detect_horizontal_symmetry(grid):
    grid_dim = grid.shape
    midline = grid_dim[0] // 2
    
    for row in range(midline):
        symmetric_row = grid_dim[0] - row - 1
        if not np.array_equal(grid[row, :], grid[symmetric_row, :]):
            return False
    return True

def highlight_adjacent(output_grid, obj):
    adjacent_color = Color.ORANGE
    n, m = obj.shape
    obj_mask = obj != Color.BLACK
    for x, y in np.argwhere(obj_mask):
        if x > 0 and obj[x-1, y] == Color.BLACK:
            output_grid[x-1, y] = adjacent_color
        if x < n-1 and obj[x+1, y] == Color.BLACK:
            output_grid[x+1, y] = adjacent_color
        if y > 0 and obj[x, y-1] == Color.BLACK:
            output_grid[x, y-1] = adjacent_color
        if y < m-1 and obj[x, y+1] == Color.BLACK:
            output_grid[x, y+1] = adjacent_color

def generate_input():
    n = np.random.randint(10, 28)
    input_grid = np.full((n, n), Color.BLACK)
    
    def random_symmetric_object():
        obj_size = np.random.randint(3, 7)
        obj_half = np.random.choice(list(Color.NOT_BLACK), size=(obj_size // 2, obj_size))
        obj = np.vstack([obj_half, obj_half[::-1]])
        return obj

    def random_non_symmetric_object():
        obj_size = np.random.randint(3, 7)
        obj = np.random.choice(list(Color.NOT_BLACK), size=(obj_size, obj_size))
        return obj

    try:
        for _ in range(np.random.randint(2, 5)):
            obj = random_symmetric_object() if np.random.rand() < 0.5 else random_non_symmetric_object()
            x, y = random_free_location_for_object(input_grid, obj, padding=1)
            blit(input_grid, obj, x, y)
    except ValueError:
        return generate_input()
    
    return input_grid