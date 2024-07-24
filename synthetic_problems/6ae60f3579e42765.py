import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, pixel manipulation, occlusion, bitmasks with separator

# description:
# In the input you will see two blue bitmasks separated by a grey horizontal bar.
# Some pixels of the bitmasks might be occluded by black pixels.
# To make the output, perform a logical OR operation between the non-black pixels of the bitmasks
# and color the resultant pixels with yellow.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey horizontal bar. Horizontal means constant Y
    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.GREY):
            break

    top_mask = input_grid[:, :y_bar]
    bottom_mask = input_grid[:, y_bar+1:]

    output_grid = np.zeros_like(top_mask)
    output_grid[
        (top_mask != Color.BLACK) | (bottom_mask != Color.BLACK)
    ] = Color.YELLOW
    
    return output_grid


def generate_input() -> np.ndarray:
    width, height = np.random.randint(2, 10), np.random.randint(2, 10)

    grid1 = np.zeros((width, height), dtype=int)
    grid2 = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            grid1[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
    
    # Create a grey horizontal bar
    bar = np.zeros((width, 1), dtype=int)
    bar[:, 0] = Color.GREY

    grid = np.concatenate((grid1, bar, grid2), axis=1)

    return grid