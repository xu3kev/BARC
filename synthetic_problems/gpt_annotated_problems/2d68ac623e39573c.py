from common import *

import numpy as np
from typing import *

# concepts:
# counting, proximity

# description:
# In the input, you will see multiple 3x3 squares of various colors and single pixels of different colors scattered around.
# To produce the output, create a 5x5 grid where each cell represents a color. 
# For each color present in the input, count how many single pixels of that color are within a 2-pixel Manhattan distance of any 3x3 square of the same color.
# Fill the corresponding cell in the output grid with that color, with the count represented by the position in the grid (left to right, top to bottom).
# If there are more than 25 colors with nearby pixels, only show the top 25 counts.

def main(input_grid):
    output_grid = np.full((5, 5), Color.BLACK)
    color_counts = {}

    # Find all 3x3 squares
    squares = []
    for x in range(input_grid.shape[0] - 2):
        for y in range(input_grid.shape[1] - 2):
            if np.all(input_grid[x:x+3, y:y+3] == input_grid[x, y]) and input_grid[x, y] != Color.BLACK:
                squares.append((x, y, input_grid[x, y]))

    # Count nearby pixels for each color
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            pixel_color = input_grid[x, y]
            if pixel_color == Color.BLACK:
                continue
            for sx, sy, square_color in squares:
                if pixel_color == square_color and np.abs(x - sx) + np.abs(y - sy) <= 2:
                    color_counts[pixel_color] = color_counts.get(pixel_color, 0) + 1
                    break

    # Sort colors by count and fill output grid
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:25]
    for i, (color, count) in enumerate(sorted_colors):
        output_grid[i // 5, i % 5] = color

    return output_grid

def generate_input():
    grid_size = random.randint(20, 30)
    grid = np.full((grid_size, grid_size), Color.BLACK)

    # Generate 3x3 squares
    colors = list(Color.NOT_BLACK)
    random.shuffle(colors)
    for color in colors[:random.randint(3, 8)]:
        square = np.full((3, 3), color)
        x, y = random_free_location_for_sprite(grid, square, padding=2)
        blit_sprite(grid, square, x, y)

    # Add scattered pixels
    for _ in range(random.randint(30, 50)):
        color = random.choice(colors)
        pixel = np.full((1, 1), color)
        x, y = random_free_location_for_sprite(grid, pixel)
        blit_sprite(grid, pixel, x, y)

    return grid