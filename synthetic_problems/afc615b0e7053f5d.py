from common import *

import numpy as np
from typing import *

# concepts:
# reflection, axis, geometric transformation

# description:
# In the input, you will see objects scattered on a grid, divided into two parts by a vertical or horizontal line.
# Your task is to reflect the objects from one side of the dividing line to the other side, creating their mirror images.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid to transform.
    output_grid = np.copy(input_grid)
    
    # Detect the dividing line (either vertical or horizontal).
    vertical_divider = False
    for row in range(input_grid.shape[0]):
        if np.all(input_grid[row, :] == Color.BLACK):
            divider_row = row
            vertical_divider = False
            break
    if not vertical_divider:
        for col in range(input_grid.shape[1]):
            if np.all(input_grid[:, col] == Color.BLACK):
                divider_col = col
                vertical_divider = True
                break

    # Reflect objects across the detected line.
    if vertical_divider:
        for row in range(input_grid.shape[0]):
            for col in range(divider_col + 1, input_grid.shape[1]):
                if input_grid[row, col] != Color.BLACK:
                    output_grid[row, 2 * divider_col - col] = input_grid[row, col]
    else:
        for row in range(divider_row + 1, input_grid.shape[0]):
            for col in range(input_grid.shape[1]):
                if input_grid[row, col] != Color.BLACK:
                    output_grid[2 * divider_row - row, col] = input_grid[row, col]
    
    return output_grid


def generate_input() -> np.ndarray:
    # Create a random size grid.
    height, width = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.zeros((height, width), dtype=int)
    
    # Add a vertical or horizontal dividing line made of black pixels.
    if np.random.rand() < 0.5:
        # Vertical line.
        divider_col = np.random.randint(5, width - 5)
        grid[:, divider_col] = Color.BLACK
        vertical_divider = True
    else:
        # Horizontal line.
        divider_row = np.random.randint(5, height - 5)
        grid[divider_row, :] = Color.BLACK
        vertical_divider = False
    
    # Place random objects on one side of the divider.
    colors = random.sample(Color.NOT_BLACK, 3)
    num_objects = np.random.randint(3, 7)
    
    for _ in range(num_objects):
        obj_height = np.random.randint(1, 4)
        obj_width = np.random.randint(1, 4)
        color = random.choice(colors)
        random_sprite_to_add = random_sprite(obj_height, obj_width, symmetry='not_symmetric', color_palette=[color])
        if vertical_divider:
            x = np.random.randint(0, height - obj_height)
            y = np.random.randint(0, divider_col - obj_width)
        else:
            x = np.random.randint(0, divider_row - obj_height)
            y = np.random.randint(0, width - obj_width)
        blit(grid, random_sprite_to_add, x, y)
    
    return grid