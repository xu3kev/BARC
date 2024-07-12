import numpy as np
from typing import *
from common import *

# concepts:
# borders, symmetry detection, reflection

# description:
# In the input grid, you will see several smaller shapes reflected horizontally or vertically on the grid.
# To create the output grid, detect each symmetric shape and draw a border around each one with a one-pixel thick yellow line.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    output_grid = input_grid.copy()

    def find_reflections(grid):
        shapes = []
        visited = np.zeros_like(grid, dtype=bool)

        def is_symmetric(shape, direction):
            if direction == 'horizontal':
                return np.all(shape == np.flip(shape, axis=1))
            if direction == 'vertical':
                return np.all(shape == np.flip(shape, axis=0))

        def dfs(x, y, color):
            stack = [(x, y)]
            shape_coords = set()
            while stack:
                cx, cy = stack.pop()
                if 0 <= cx < n and 0 <= cy < m and not visited[cx, cy] and grid[cx, cy] == color:
                    visited[cx, cy] = True
                    shape_coords.add((cx, cy))
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        stack.append((cx+dx, cy+dy))
            return shape_coords

        for i in range(n):
            for j in range(m):
                if not visited[i, j] and input_grid[i, j] != Color.BLACK:
                    color = input_grid[i, j]
                    shape_coords = dfs(i, j, color)
                    min_x, min_y = np.min(list(shape_coords), axis=0)
                    max_x, max_y = np.max(list(shape_coords), axis=0)
                    shape = input_grid[min_x:max_x+1, min_y:max_y+1]
                    if is_symmetric(shape, 'horizontal') or is_symmetric(shape, 'vertical'):
                        shapes.append(((min_x, min_y), (max_x, max_y)))
        return shapes

    shapes = find_reflections(input_grid)
    for (min_x, min_y), (max_x, max_y) in shapes:
        draw_line(output_grid, min_x, min_y, length=(max_x-min_x), color=Color.YELLOW, direction=(1,0))
        draw_line(output_grid, max_x, min_y, length=(max_y-min_y), color=Color.YELLOW, direction=(0,1))
        draw_line(output_grid, min_x, min_y, length=(max_y-min_y), color=Color.YELLOW, direction=(0,1))
        draw_line(output_grid, min_x, max_y, length=(max_x-min_x), color=Color.YELLOW, direction=(1,0))

    return output_grid

def generate_input() -> np.ndarray:
    grid_size = np.random.randint(10, 15)
    input_grid = np.full((grid_size, grid_size), Color.BLACK)
    num_shapes = np.random.randint(2, 5)

    for _ in range(num_shapes):
        shape_size = np.random.randint(2, 5)
        shape = random_sprite(shape_size, shape_size, color_palette=random.sample(list(Color.NOT_BLACK),2))
        x, y = np.random.randint(0, grid_size - shape_size, 2)

        if np.random.rand() < 0.5:
            shape = np.flip(shape, axis=1)  # Horizontal reflection
        if np.random.rand() < 0.5:
            shape = np.flip(shape, axis=0)  # Vertical reflection
        
        for i in range(shape_size):
            for j in range(shape_size):
                input_grid[x + i, y + j] = shape[i, j]

    return input_grid