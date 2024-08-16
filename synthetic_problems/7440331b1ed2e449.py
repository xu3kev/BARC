import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, reflection 

# description:
# In the input, you will see two horizontal blue bitmasks separated by a grey horizontal bar.
# To produce the output, color green the red that are set in either bitmask (logical OR), and reflect one bitmask to the opposite side of the bar to create a mirror effect.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey horizontal bar. Horizontal means constant Y.
    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.GREY):
            break

    top_mask = input_grid[:, :y_bar]
    bottom_mask = input_grid[:, y_bar+1:]

    # Logical OR of the two bitmasks
    output_grid = np.zeros_like(top_mask)
    output_grid[(top_mask == Color.BLUE) | (bottom_mask == Color.BLUE)] = Color.GREEN
    
    # Reflect the bottom mask to the top and vice versa
    reflected_top_mask = np.flipud(bottom_mask)
    reflected_bottom_mask = np.flipud(top_mask)

    # Create the final result grid with the bar in the middle
    result_grid = np.concatenate((reflected_top_mask, np.full((input_grid.shape[0], 1), Color.GREY), reflected_bottom_mask), axis=1)

    return result_grid


def generate_input() -> np.ndarray:
    # Create a pair of equally sized blue bitmasks with a grey separator bar horizontally
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