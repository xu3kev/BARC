from common import *
import numpy as np
from typing import *

# concepts:
# Pixels manipulation, color guide, scaling

# description:
# In the input, you will see a grid with colored pixels and a colored rectangular border around each color. The rectangular border can vary in thickness and can be up to 2 squares wide.
# To make the output, upscale the grid so that each pixel becomes a 3x3 block where each block has the same color as the original pixel. Pixels within rectangular borders should become outlined blocks with the same color as the original rectangular border.

def main(input_grid):
    thickness = 2  # Thickness of the border
    upscale_factor = 3  # Upscale factor for each pixel

    n, m = input_grid.shape
    output_grid = np.zeros((n * upscale_factor, m * upscale_factor), dtype=int)

    for i in range(n):
        for j in range(m):
            color = input_grid[i, j]

            # Determine if this pixel is within a rectangular border
            border_x_range = list(range(max(0, i - thickness), min(n, i + thickness + 1)))
            border_y_range = list(range(max(0, j - thickness), min(m, j + thickness + 1)))
  
            is_border_pixel = any(
                input_grid[x, j] == color or input_grid[i, y] == color for x in border_x_range for y in border_y_range if input_grid[x, y] != color
            )

            if is_border_pixel:
                for x in range(i * upscale_factor, (i + 1) * upscale_factor):
                    for y in range(j * upscale_factor, (j + 1) * upscale_factor):
                        if x in [i * upscale_factor, (i + 1) * upscale_factor - 1] or y in [j * upscale_factor, (j + 1) * upscale_factor - 1]:
                            output_grid[x, y] = color
            else:
                output_grid[
                    i * upscale_factor : (i + 1) * upscale_factor, j * upscale_factor : (j + 1) * upscale_factor
                ] = color

    return output_grid

def generate_input():
    n, m = np.random.randint(5, 10, size=2)
    input_grid = np.zeros((n, m), dtype=int)

    num_colors = np.random.randint(3, 6)
    colors = random.sample(list(Color.NOT_BLACK), num_colors)

    for color_index, color in enumerate(colors):
        n_pixels = np.random.randint(1, 4)

        for _ in range(n_pixels):
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            input_grid[x, y] = color

    return input_grid