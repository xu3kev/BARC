from common import *

import numpy as np
from typing import *


# concepts:
# path finding, flood fill, color replacement

# description:
# In the input, you will see a grid with a black background and colored pixels sprinkled on it.
# The task is to flood fill each colored pixel with a distance-based gradient, which means the farther the pixel is from the starting pixel, 
# the more it blends with a specific target color.
# To make the output, execute the flood fill from every unique colored pixel.

def main(input_grid: np.ndarray) -> np.ndarray:
    target_color = Color.TEAL
    
    distances = np.full_like(input_grid, fill_value=-1)  # Initialize with -1
    
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] != Color.BLACK:
                flood_fill_distances(distances, x, y, input_grid)

    output_grid = input_grid.copy()

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if distances[x, y] != -1:
                distance = distances[x, y]
                blend_color = blend(input_grid[x, y], target_color, distance)
                output_grid[x, y] = blend_color
                
    return output_grid

def flood_fill_distances(distances, start_x, start_y, input_grid):
    queue = [(start_x, start_y)]
    distances[start_x, start_y] = 0
    color = input_grid[start_x, start_y]
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y = queue.pop(0)
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1] and distances[nx, ny] == -1 and input_grid[nx, ny] == Color.BLACK:
                distances[nx, ny] = distances[x, y] + 1
                queue.append((nx, ny))

def blend(color1, color2, weight):
    # Just a placeholder blending function, does not actually blend colors correctly.
    # Should be replaced with proper blending logic.
    return color1 if weight < 5 else color2

def generate_input() -> np.ndarray:
    grid = np.full((15, 15), fill_value=Color.BLACK)
    
    num_colors = random.randint(3, 5)
    colors = random.sample(Color.NOT_BLACK, num_colors)

    for _ in range(num_colors):
        x = random.randint(0, grid.shape[0]-1)
        y = random.randint(0, grid.shape[1]-1)
        color = random.choice(colors)
        grid[x, y] = color

    return grid