from common import *

import numpy as np
from typing import *

def main(input_grid):
    # Create a copy of the input grid for the output
    output_grid = np.copy(input_grid)

    # Find the different base pixel color
    colors, counts = np.unique(input_grid, return_counts=True)
    base_color = colors[np.argmin(counts)]

    # Find the location of the base pixel
    base_x, base_y = np.argwhere(input_grid == base_color).flatten()

    # Grow a vertical bar upwards from the base pixel
    for i in range(base_x, -1, -1):
        if output_grid[i, base_y] != Color.BLACK:
            break
        output_grid[i, base_y] = base_color

    # Calculate the central vertical axis of the grid
    center_y = input_grid.shape[1] // 2

    # Reflect the bar across the central vertical axis
    for i in range(output_grid.shape[0]):
        if output_grid[i, base_y] == base_color:
            reflected_y = 2 * center_y - base_y
            if 0 <= reflected_y < output_grid.shape[1]:
                output_grid[i, reflected_y] = base_color

    return output_grid

def generate_input():
    # Choose a random size for the triangle
    size = np.random.randint(2, 5)
    width = size * 2 + 1
    height = size + 1

    # Choose random colors for the triangle and the base pixel
    triangle_color = np.random.choice(Color.NOT_BLACK)
    base_color = np.random.choice(Color.NOT_BLACK)
    
    while base_color == triangle_color:
        base_color = np.random.choice(Color.NOT_BLACK)

    # Create a triangle on a black grid
    triangle_sprite = np.zeros((height, width), dtype=int)
    
    for i in range(height):
        for j in range(size - i, size + i + 1):
            triangle_sprite[i, j] = triangle_color

    # Set the base pixel color
    triangle_sprite[height-1, size] = base_color

    # Create a larger black grid for the background
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Place the triangle on the grid ensuring it fits within bounds
    x, y = np.random.randint(1, n - height), np.random.randint(1, m - width)
    blit_sprite(grid, triangle_sprite, x, y)

    return grid