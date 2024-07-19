from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects, repetition, connecting colors

# description:
# In the input, you will see a chevron-shaped object of one color and several pairs of adjacent pixels of other different colors scattered through the grid.
# For each pair of colored pixels, create a chevron with these colors and slide the chevron downwards until it reaches the bottom of the grid or encounters another already placed chevron.

def main(input_grid):
    # Copy the input to the output grid
    output_grid = np.copy(input_grid)

    # Get the chevron's color and shape
    shapes = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    original_chevron = max(shapes, key=lambda s: np.count_nonzero(s))
    chevron_color = original_chevron[original_chevron != Color.BLACK][0]

    # Detect pairs of adjacent pixels with different colors
    pairs = []
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1] - 1):  # Check right-adjacent pixel
            if input_grid[x, y] != Color.BLACK and input_grid[x, y+1] != Color.BLACK:
                pairs.append(((x, y), (x, y+1)))

    chevrons_to_add = []
    for ((x1, y1), (x2, y2)) in pairs:
        chevron_color1, chevron_color2 = input_grid[x1, y1], input_grid[x2, y2]
        new_chevron = np.full((7, 4), Color.BLACK)
        new_chevron[3, 0] = chevron_color1
        new_chevron[2:5, 1] = chevron_color1
        new_chevron[1:6, 2] = chevron_color2
        new_chevron[0:7, 3] = chevron_color2
        chevrons_to_add.append((new_chevron, x1, y1))

    for chevron, cx, cy in chevrons_to_add:
        bx, by = cx, cy  # bottom-x, bottom-y coordinates for current chevron
        while can_slide_down(output_grid, chevron, bx, by):
            bx += 1
        blit_sprite(output_grid, chevron, bx, by, background=Color.BLACK)

    return output_grid

def can_slide_down(grid, chevron, x, y):
    if x + chevron.shape[0] >= grid.shape[0]:
        return False
    for dx in range(chevron.shape[0]):
        for dy in range(chevron.shape[1]):
            if chevron[dx, dy] != Color.BLACK and grid[x + dx + 1, y + dy] != Color.BLACK:
                return False
    return True

def generate_input():
    input_grid = np.full((20, 20), Color.BLACK)

    chevron_color = np.random.choice(Color.NOT_BLACK)

    # Create the original chevron
    chevron = np.full((7, 4), Color.BLACK)
    chevron[3, 0] = chevron_color
    chevron[2:5, 1] = chevron_color
    chevron[1:6, 2] = chevron_color
    chevron[0:7, 3] = chevron_color

    # Place the original chevron in the grid
    x, y = np.random.randint(0, 14), np.random.randint(0, 16)
    blit_sprite(input_grid, chevron, x, y)

    # Generate random pairs of adjacent pixels
    n_pairs = np.random.randint(5, 25)
    for _ in range(n_pairs):
        px, py = np.random.randint(0, 20), np.random.randint(0, 19)
        color1, color2 = np.random.choice(Color.NOT_BLACK, 2, replace=False)
        input_grid[px, py] = color1
        if py + 1 < 20:
            input_grid[px, py + 1] = color2

    return input_grid