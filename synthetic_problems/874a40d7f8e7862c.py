from common import *

import numpy as np
from typing import *

# concepts:
# sorting, color change, size, proximity

# description:
# In the input you will see a grid with a single blue pixel and a row of 4 grey bars of different heights, each starting at the bottom of the canvas, and each separated by 1 pixel (so they are two pixels apart)
# Color the bar closest to the blue pixel yellow, the second closest one green, the third closest one red, and the farthest one blue.

def main(input_grid):
    # Find the blue pixel
    blue_pixel_pos = np.argwhere(input_grid == Color.BLUE)[0]
    blue_x, blue_y = blue_pixel_pos
    
    # extract the bars, each of which is a connected component
    bars = find_connected_components(input_grid, background=Color.BLACK)

    # sort the bars by the distance to the blue pixel
    bars_with_distances = [(bar, min([abs(x-blue_x) + abs(y-blue_y) for x, y in np.argwhere(bar != Color.BLACK)])) for bar in bars]
    bars_with_distances.sort(key=lambda x: x[1])  # sorting by distance
    
    # bars sorted by distance
    sorted_bars = [item[0] for item in bars_with_distances]
    
    output_grid = input_grid.copy()
    
    closest_bar = sorted_bars[0]
    closest_bar_mask = closest_bar != Color.BLACK
    output_grid[closest_bar_mask] = Color.YELLOW

    second_closest_bar = sorted_bars[1]
    second_closest_bar_mask = second_closest_bar != Color.BLACK
    output_grid[second_closest_bar_mask] = Color.GREEN

    third_closest_bar = sorted_bars[2]
    third_closest_bar_mask = third_closest_bar != Color.BLACK
    output_grid[third_closest_bar_mask] = Color.RED
    
    farthest_bar = sorted_bars[3]
    farthest_bar_mask = farthest_bar != Color.BLACK
    output_grid[farthest_bar_mask] = Color.BLUE
    
    return output_grid

def generate_input():
    # make a black 9x9 grid
    n, m = 9, 9
    grid = np.zeros((9, 9), dtype=int)
    
    # place a single blue pixel randomly on the grid
    blue_x, blue_y = np.random.randint(0, n), np.random.randint(0, m)
    grid[blue_x, blue_y] = Color.BLUE
    
    # pick 4 distinct heights (between 1 and 9), ensuring unique heights
    heights = random.sample(range(1, 9), 4)
    
    # draw the bars
    # space them by 2 so that there is a black pixel in between each pair
    for i, height in enumerate(heights):
        grid[:, i*2] = [Color.BLACK]*(n - height) + [Color.GREY]*height
    
    return grid