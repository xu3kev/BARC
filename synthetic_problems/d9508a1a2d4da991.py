import numpy as np
from typing import *
from common import *

# concepts:
# objects, alignment by color, bitmasks with separator, boolean logical operations

# description:
# In the input you will see two grids separated by a blue vertical bar. The left grid acts as a stencil mask where yellow pixels are the stencil.
# The right grid contains objects of varying colors.
# In the output grid, pixels in the right grid are turned teal if they correspond to yellow pixels in the stencil.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the blue vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.BLUE):
            break

    stencil_mask = input_grid[:x_bar, :]
    object_grid = input_grid[x_bar+1:, :]

    # Create output grid which initially is a copy of the object grid
    output_grid = np.copy(object_grid)

    # Apply the stencil: if the corresponding pixel in the stencil_mask is yellow, turn the pixel teal in the output
    teal_pixels = np.argwhere(stencil_mask == Color.YELLOW)
    
    for x, y in teal_pixels:
        if x < output_grid.shape[0] and y < output_grid.shape[1]:
            output_grid[x, y] = Color.TEAL

    return output_grid

def generate_input() -> np.ndarray:
    # Create two equally sized grids
    width, height = np.random.randint(5, 10), np.random.randint(5, 10)

    # Generate the stencil mask
    stencil_mask = np.zeros((width, height), dtype=int)
    colors = list(Color.NOT_BLACK)
    
    # Create random patterns with a specific frequency of yellow
    for x in range(width):
        for y in range(height):
            if np.random.random() < 0.2:  # 20% chance to be yellow
                stencil_mask[x, y] = Color.YELLOW
            else:
                stencil_mask[x, y] = Color.BLACK

    # Generate the object grid
    object_grid = np.zeros((width, height), dtype=int)
    for x in range(width):
        for y in range(height):
            object_color = np.random.choice(colors)
            object_grid[x, y] = object_color

    # Create a blue vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.BLUE

    # Combine the grids
    grid = np.concatenate((stencil_mask, bar, object_grid), axis=0)
    
    return grid