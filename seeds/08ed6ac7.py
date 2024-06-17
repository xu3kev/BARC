from common import *

import numpy as np
from typing import *

# concepts:
# sorting, color change, size

# description:
# In the input you will see a row of exactly 4 grey bars of different heights, each starting at the bottom of the canvas, and each separated by 1 pixel (so they are two pixels apart)
# Color the tallest one blue, the second tallest one red, the third tallest one green, and the shortest one yellow.

def main(input_grid):

    # extract the bars, each of which is a connected component
    bars = find_connected_components(input_grid, background=Color.BLACK)

    # sort the bars by height
    bars = list(sorted(bars, key=lambda bar: np.sum(bar != Color.BLACK), reverse=True))

    # color the bars
    output_grid = input_grid.copy()

    biggest_bar = bars[0]
    biggest_bar_mask = biggest_bar != Color.BLACK
    output_grid[biggest_bar_mask] = Color.BLUE

    second_biggest_bar = bars[1]
    second_biggest_bar_mask = second_biggest_bar != Color.BLACK
    output_grid[second_biggest_bar_mask] = Color.RED

    third_biggest_bar = bars[2]
    third_biggest_bar_mask = third_biggest_bar != Color.BLACK
    output_grid[third_biggest_bar_mask] = Color.GREEN

    smallest_bar = bars[3]
    smallest_bar_mask = smallest_bar != Color.BLACK
    output_grid[smallest_bar_mask] = Color.YELLOW

    return output_grid



def generate_input():
    # make a black 9x9 grid
    n, m = 9, 9
    grid = np.zeros((9, 9), dtype=int)

    # pick 4 distinct heights (can't reuse the same height)
    heights = random.sample(range(1, 9), 4)

    # draw the bars
    # space them by 2 so that there is a black pixel in between each pair
    for i, height in enumerate(heights):
        grid[1+i*2, -height:] = Color.GREY
        
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)