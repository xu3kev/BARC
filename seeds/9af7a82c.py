from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# The input grid consists of a small grid filled with different colors.
# To create the output grid, take the colors present in the input, and sort them by number of pixels of that color in the input, greatest to least. Then create an output grid of shape (num_colors, max_num_pixels), where each row is filled with the color corresponding to that row's index in the sorted list of colors. If a color has fewer pixels than max_num_pixels, fill the remaining pixels with black.

def main(input_grid):
    # find all unique colors in the input grid
    colors = np.unique(input_grid)
    colors = colors[colors != Color.BLACK]

    colors_with_counts = [(c, np.sum(input_grid == c)) for c in colors]
    sorted_colors_with_counts = sorted(colors_with_counts, key=lambda x: x[1], reverse=True)

    # create an output grid of shape (num_colors, max_num_pixels)
    num_colors = len(colors)
    max_num_pixels = max([count for c, count in sorted_colors_with_counts])
    output_grid = np.full((num_colors, max_num_pixels), Color.BLACK)

    # fill each row with the color corresponding to that row's index in the sorted list of colors
    for i, (color, count) in enumerate(sorted_colors_with_counts):
        output_grid[i, :count] = color

    return output_grid


def generate_input():
    # create a small grid (3-5 x 3-5)
    input_grid = np.full((np.random.randint(3, 6), np.random.randint(3, 6)), Color.BLACK)

    # while there are black pixels remaining, choose a random color, choose a random number of pixels to color with that color, and color those pixels
    while True:
        if np.sum(input_grid == Color.BLACK) == 0:
            break

        color = np.random.choice(Color.NOT_BLACK)
        num_pixels = np.random.randint(1, min(np.sum(input_grid == Color.BLACK) + 1, 6))
        # choose num_pixels random black pixels to color with the chosen color
        choices = np.argwhere(input_grid == Color.BLACK)
        pixels = np.random.choice(len(choices), num_pixels, replace=False)
        for pixel in pixels:
            x, y = choices[pixel]
            input_grid[x, y] = color

    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

