from common import *

import numpy as np
from typing import *

# concepts:
# Manhattan distance, color propagation, influence fields

# description:
# Given an input grid, each non-black pixel will generate a surrounding field of influence where pixels are colored based on their Manhattan distance to the nearest non-black pixel.
# The main transformation involves coloring each pixel in the grid based on the color and adjacency (Manhattan distance) to the nearby colored pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.full_like(input_grid, Color.BLACK)

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] != Color.BLACK:
                propagate_color(output_grid, input_grid[x, y], x, y)
    
    return output_grid

def propagate_color(grid: np.ndarray, color: str, center_x: int, center_y: int) -> None:
    max_distance = (grid.shape[0] + grid.shape[1] - 2)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == Color.BLACK:
                distance = abs(center_x - x) + abs(center_y - y)
                if distance <= max_distance:
                    grid[x, y] = color

def generate_input() -> np.ndarray:
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.full((n, m), Color.BLACK)
    
    num_colored_pixels = np.random.randint(2, 6)
    for _ in range(num_colored_pixels):
        pixel_color = np.random.choice(list(Color.NOT_BLACK))
        sprite = np.array([pixel_color]).reshape(1, 1)
        x, y = random_free_location_for_object(grid, sprite)
        blit(grid, sprite, x, y)
    
    return grid

# Example usage and testing