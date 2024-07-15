from common import *

import numpy as np
from typing import *

# concepts:
# counting, incrementing, filling, objects

# description:
# In the input, you will see a grid with a single colored object and a sequence of colored pixels in the bottom row.
# Each colored pixel specifies the number of vertical layers that need to grow upward from the bottommost row.
# To make the output: 
# 1. Identify the colored object and bottom row sequence from the input grid.
# 2. Add layers to the object in the respective columns based on the number of colored pixels.
# 3. Keep track of boundaries to avoid overlap in the case that layers expand horizontally within the object.


def main(input_grid):
    # Create a copy of the input grid to work with
    output_grid = np.copy(input_grid)

    # Get the color of the bottom row sequence
    bottom_row_colors = input_grid[-1, :]
    
    # Get unique colors from the sequence, excluding the background color
    unique_colors = [color for color in np.unique(bottom_row_colors) if color != Color.BLACK]

    # Iterate over columns of the bottom row and grow the object accordingly
    for col in range(input_grid.shape[1]):
        color = bottom_row_colors[col]

        if color != Color.BLACK:
            # Find the length of vertical sequence to add
            layer_length = np.count_nonzero(bottom_row_colors == color)

            # Expand object in the respective column
            for row in range(input_grid.shape[0]):
                if input_grid[row, col] != Color.BLACK:
                    for offset in range(1, layer_length + 1):
                        if row - offset >= 0:
                            output_grid[row - offset, col] = color
                        else:
                            break
                    break

    return output_grid


def generate_input():
    # Create dimensions for the grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Choose colors for the object and the bottom row sequence
    object_color = random.choice(list(Color.NOT_BLACK))
    sequence_colors = [random.choice(list(Color.NOT_BLACK)) for _ in range(m)]

    # Ensure no BLACK colors in sequence
    sequence_colors = [color if color != Color.BLACK else random.choice(list(Color.NOT_BLACK)) for color in sequence_colors]

    # Create a random object and place it in the middle of the grid
    sprite = random_sprite(np.random.randint(2, n-2), np.random.randint(2, m-2), density=0.5, symmetry="not_symmetric", color_palette=[object_color])
    sprite_x, sprite_y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x=sprite_x, y=sprite_y)

    # Place the color sequence in the bottom row
    for idx, color in enumerate(sequence_colors):
        grid[-1, idx] = color

    return grid