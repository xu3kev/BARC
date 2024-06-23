from common import *

import numpy as np
from typing import *

# concepts:
# repeating pattern, connecting colors

# description:
# In the input grid, you will see an all black grid with three dots of the same color in a perfect 45 degree diagonal, but equally spaced apart from each other.
# To create the output grid, connect the outer two of the three dots with a square border shape. The square border contains the two dots as corners, and is centered on the third center dot. Then make another square border that is the same distance (number of background cells) from the existing border as the existing border is from the center dot. Repeat making square borders of the same distance outwards until the grid is filled.

def main(input_grid):
    # Plan:
    # 1. get the dots
    # 2. get the center dot, and the two outer dots
    # 3. calculate the distance from the center dot of the outer dots.
    # 4. make a helper function for drawing a square of a certain distance from the center dot
    # 5. repeat making squares of multiples of that distance until no new cells are filled in on the grid.

    # get a list of locations
    pixel_xs, pixel_ys = np.where(input_grid != Color.BLACK)
    pixel_locations = list(zip(list(pixel_xs), list(pixel_ys)))
    assert len(pixel_locations) == 3
    
    # sort by x coordinate
    pixel0, pixel1, pixel2 = sorted(pixel_locations, key=lambda l: l[0])
    color = input_grid[pixel0[0], pixel0[1]]
    width = pixel1[0] - pixel0[0]

    def in_bounds(grid, x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def draw_square_border(grid, x, y, w, h, color):
        # x, y is the top left corner
        for dx in range(w+1):
            # top border
            if in_bounds(grid, x+dx, y):
                grid[x+dx, y] = color
            # bottom border
            if in_bounds(grid, x+dx, y+h):
                grid[x+dx, y+h] = color
        for dy in range(h+1):
            # left border
            if in_bounds(grid, x, y+dy):
                grid[x, y+dy] = color
            # right border
            if in_bounds(grid, x+w, y+dy):
                grid[x+w, y+dy] = color

    output_grid = input_grid.copy()
    i = 1
    while True:
        top_left_x = pixel1[0] - width * i
        top_left_y = pixel1[1] - width * i
        w = 2 * (width * i)
        old_grid = output_grid.copy()
        draw_square_border(output_grid, top_left_x, top_left_y, w, w, color)
        if not np.any(old_grid != output_grid):
            break
        i += 1

    return output_grid

def generate_input():
    # 1. make a 28x28 black grid
    # 2. choose a distance from the center between 1 and 10
    # 3. make the three initial dots on a grid
    # 4. blit onto a random spot on the black grid
    input_grid = np.full((28,28), Color.BLACK)
    distance = np.random.randint(2, 11)
    color = np.random.choice(Color.NOT_BLACK)
    center_x = np.random.randint(distance, 28 - distance)
    center_y = np.random.randint(distance, 28 - distance)
    input_grid[center_x, center_y] = color
    input_grid[center_x - distance, center_y - distance] = color
    input_grid[center_x + distance, center_y + distance] = color
    # randomly rotate the input grid sometimes
    if np.random.rand() < 0.55:
        input_grid = np.rot90(input_grid)

    return input_grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
