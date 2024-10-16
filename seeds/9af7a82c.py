from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# The input grid consists of a small grid filled completely with different colors.
# To create the output grid, take the colors present in the input, and sort them by number of pixels of that color in the input, greatest to least. Then create an output grid of shape (num_colors, max_num_pixels), where num_colors is the number of colors in the input, and max_num_pixels is the max number of pixels of any color in the input. Then fill each row with the color corresponding to that row's index in the sorted list of colors, filling K pixels from the top downwards, where K is the number of pixels of that color in the input. Leave the remaining pixels in the row black.

def main(input_grid):
    # find all unique colors in the input grid
    colors = np.unique(input_grid)

    # track the number of pixels of each color in the input grid
    colors_with_counts = [(c, np.sum(input_grid == c)) for c in colors]
    sorted_colors_with_counts = sorted(colors_with_counts, key=lambda x: x[1], reverse=True)

    # create an output grid of shape (num_colors, max_num_pixels)
    num_colors = len(colors)
    max_num_pixels = max([count for _, count in sorted_colors_with_counts])
    output_grid = np.full((num_colors, max_num_pixels), Color.BLACK)

    # for each color in the list, color K pixels to that color from top to bottom, leaving the remaining pixels black, where K is the number of pixels of that color in the input.
    for i, (color, count) in enumerate(sorted_colors_with_counts):
        output_grid[i, :count] = color

    return output_grid


def generate_input():
    # create a small grid (3-5 x 3-5)
    input_grid = np.full((np.random.randint(3, 6), np.random.randint(3, 6)), Color.BLACK)

    # while there are black pixels remaining, choose a random color, choose a random number of pixels to color with that color, and color those pixels
    while True:
        # if there are no black pixels remaining, we're done
        if np.sum(input_grid == Color.BLACK) == 0:
            break

        # choose a random color and number of pixels to color with that color
        color = np.random.choice(Color.NOT_BLACK)
        num_pixels = np.random.randint(1, min(np.sum(input_grid == Color.BLACK) + 1, 6))

        # choose num_pixels random black pixels to color with the chosen color
        choices = np.argwhere(input_grid == Color.BLACK)
        pixels = np.random.choice(len(choices), num_pixels, replace=False)

        # color the chosen pixels
        for pixel in pixels:
            x, y = choices[pixel]
            input_grid[x, y] = color

    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

