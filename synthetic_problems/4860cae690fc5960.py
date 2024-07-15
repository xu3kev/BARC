from common import *

import numpy as np
from typing import *

# concepts:
# connecting colors, repeating pattern, geometry

# description:
# In the input grid, you will see three dots forming an equilateral triangle. The vertices/dots are equally spaced apart, and all are the same color.
# To create the output grid, first connect the three vertices of the triangle with lines, forming the triangular shape. From this initial triangle, iteratively grow the triangle by adding an additional layer of colored pixels around the previous triangle.
# This growth should continue until no more new cells can fit in the grid.

def main(input_grid):
    pixel_xs, pixel_ys = np.where(input_grid != Color.BLACK)
    pixel_locations = list(zip(list(pixel_xs), list(pixel_ys)))
    assert len(pixel_locations) == 3
    
    # sort by coordinates to get the vertices of the equilateral triangle
    pixel0, pixel1, pixel2 = sorted(pixel_locations)
    color = input_grid[pixel0[0], pixel0[1]]
    distance = pixel1[0] - pixel0[0]

    output_grid = input_grid.copy()

    def draw_line(output_grid, start, end, color):
        x1, y1 = start
        x2, y2 = end
        points = zip(np.linspace(x1, x2, num=abs(x1-x2) + 1, dtype=int), np.linspace(y1, y2, num=abs(y1-y2) + 1, dtype=int))
        for x, y in points:
            if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                output_grid[x, y] = color

    def draw_triangle(grid, vertices, color):
        draw_line(grid, vertices[0], vertices[1], color)
        draw_line(grid, vertices[1], vertices[2], color)
        draw_line(grid, vertices[2], vertices[0], color)

    i = 1
    while True:
        vertices = [
            (pixel0[0] - distance * i, pixel0[1]),
            (pixel1[0], pixel1[1] - distance * i),
            (pixel2[0] + distance * i, pixel2[1]),
        ]
        
        old_grid = output_grid.copy()
        draw_triangle(output_grid, vertices, color)

        if np.array_equal(old_grid, output_grid):
            break
        i += 1

    return output_grid

def generate_input():
    input_grid = np.full((28, 28), Color.BLACK)
    distance = np.random.randint(2, 7)
    color = np.random.choice(Color.NOT_BLACK)
    center_x, center_y = np.random.randint(distance, 28 - distance), np.random.randint(distance, 28 - distance)
    
    input_grid[center_x, center_y] = color
    input_grid[center_x - distance, center_y - distance] = color
    input_grid[center_x + distance, center_y - distance] = color

    return input_grid