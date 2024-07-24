from common import *

import numpy as np
from typing import *


def main(input_grid):
    # Plan:
    # 1. Find the diagonal symmetry line
    # 2. Reflect each colored pixel across the diagonal line and fill in any missing pixels

    # get input grid shape
    n, m = input_grid.shape

    # find the diagonal symmetry line (we'll assume it's the main diagonal from top-left to bottom-right for simplicity)
    diag_line = [(i, i) for i in range(min(n, m))]

    # create the output grid by copying the input grid
    output_grid = np.copy(input_grid)

    # fill missing parts to make it diagonally symmetric
    for x in range(n):
        for y in range(m):
            if input_grid[x][y] != Color.BLACK:
                # get the color
                color = input_grid[x][y]

                # find the reflected pixel across the main diagonal
                reflected_x, reflected_y = y, x

                # if the reflected pixel is black, fill it with the same color
                if output_grid[reflected_x][reflected_y] == Color.BLACK:
                    output_grid[reflected_x][reflected_y] = color

    return output_grid


def generate_input():
    # create a 10x10 black grid for the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)

    # create a smaller randomly colored sprite with diagonal symmetry
    sprite_dim = np.random.randint(3, min(n, m) // 2)
    sprite = random_sprite(sprite_dim, sprite_dim, density=0.5, symmetry="diagonal", color_palette=list(Color.NOT_BLACK))

    # randomly remove some pixels from the sprite to simulate occlusion
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if np.random.rand() < 0.3:  # 30% chance to remove each pixel
                sprite[i, j] = Color.BLACK

    # find a random free location for the sprite and blit it onto the grid
    x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
    blit_sprite(grid, sprite, x, y)

    return grid