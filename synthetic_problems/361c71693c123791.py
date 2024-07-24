from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    # Locate the chevron by identifying the largest connected component
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    chevron = max(objects, key=lambda o: np.count_nonzero(o))

    # Identify the color of the chevron
    chevron_color = chevron[chevron != Color.BLACK][0]

    # Locate the position of the tip of the chevron
    chevron_boundary = object_boundary(chevron)
    tip_x, tip_y = np.argwhere(chevron_boundary)[0]

    # Create the output grid starting as a copy of the input grid
    output_grid = input_grid.copy()

    for x in range(input_grid.shape[0]):
        # From the tip, create vertical rectangular cells downwards
        for y in range(tip_y, input_grid.shape[1]):
            if input_grid[x, y] == Color.BLACK:
                output_grid[x, y] = chevron_color

    return output_grid

def generate_input() -> np.ndarray:
    # Generate a grid of size between 15x15 to 20x20
    n = random.randint(15, 20)
    input_grid = np.full((n, n), Color.BLACK)

    # Choose colors for the chevron and scattered pixels
    chevron_color, pixel_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # Create the chevron
    chevron = np.full((7, 4), Color.BLACK)
    x, y = np.indices(chevron.shape)
    chevron[np.logical_and(y == 0, x == 3)] = chevron_color
    chevron[np.logical_and(y == 1, np.logical_and(x >= 2, x <= 4))] = chevron_color
    chevron[np.logical_and(y == 2, np.logical_and(x >= 1, x <= 5))] = chevron_color
    chevron[np.logical_and(y == 3, np.logical_or(x == 0, x == 6))] = chevron_color

    # Position chevron in the upper half of the grid
    chevron_x, chevron_y = np.random.randint(0, n - 7), np.random.randint(0, n//2 - 4)
    blit_sprite(input_grid, chevron, x=chevron_x, y=chevron_y)

    # Scatter 5-25 pixels in the grid
    num_pixels = np.random.randint(5, 26)
    available_positions = np.argwhere(input_grid == Color.BLACK)
    scatter_positions = available_positions[np.random.choice(len(available_positions), num_pixels, replace=False)]

    for x, y in scatter_positions:
        input_grid[x, y] = pixel_color

    return input_grid