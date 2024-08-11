from common import *

import numpy as np
from typing import *

# concepts:
#  alignment, masking, puzzle piece, scaling

# description:
# In the input, you will see three rectangular monochromatic colored shapes (red, blue, yellow) on a black background. They could be at different horizontal positions.
# The output has a black background, with the three shapes horizontally aligned such that their heights are the same and they are stacked vertically without changing their original colors or shapes. The heights may change to match the tallest shape among them.

def main(input_grid):
    # Detect the three colors (red, blue, yellow) and their corresponding shapes
    color_shapes = []
    for color in (Color.RED, Color.BLUE, Color.YELLOW):
        color_coords = np.where(input_grid == color)
        if color_coords[0].size > 0:
            color_shapes.append((color, color_coords))

    # Get the height of each shape
    shape_heights = [(coords[0].max() - coords[0].min() + 1) for _, coords in color_shapes]
    max_height = max(shape_heights)

    # Create output grid with height enough to stack shapes vertically
    output_grid = np.full((max_height * len(color_shapes), input_grid.shape[1]), Color.BLACK, dtype=int)

    # Blit every shape to its new location in the output grid
    for i, (color, coords) in enumerate(color_shapes):
        shape_height = coords[0].max() - coords[0].min() + 1
        vertical_offset = i * max_height
        top_offset = vertical_offset + (max_height - shape_height) // 2
        offset_min_row = coords[0].min()
        offset_min_col = coords[1].min()
        for r, c in zip(coords[0], coords[1]):
            output_grid[top_offset + (r - offset_min_row), c] = color

    return output_grid


def generate_input():
    # Create an empty grid of sufficient size
    height = np.random.randint(10, 20)
    width = np.random.randint(15, 25)
    input_grid = np.full((height, width), Color.BLACK, dtype=int)

    # Generate random shapes for each color
    shapes = []
    for color in [Color.RED, Color.BLUE, Color.YELLOW]:
        shape_height = np.random.randint(3, 7)
        shape_width = np.random.randint(2, 5)
        shape = random_sprite(shape_height, shape_width, density=0.7, color_palette=[color])
        shape_coords = np.argwhere(shape != Color.BLACK)
        shape_coords[:, 0] += np.random.randint(0, height - shape_height)
        shape_coords[:, 1] += np.random.randint(0, width - shape_width)
        shapes.append((color, shape_coords))

    # Place shapes on the grid
    for color, coords in shapes:
        for r, c in coords:
            input_grid[r, c] = color

    return input_grid