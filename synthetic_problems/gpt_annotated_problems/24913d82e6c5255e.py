from common import *

import numpy as np
from typing import *

# concepts:
# connecting colors, repeating pattern, pixel manipulation, growing

# description:
# In the input grid, you will see three colored pixels forming an isosceles right triangle.
# To create the output grid:
# 1. Connect these three pixels with lines of their respective colors, forming a right triangle.
# 2. From each vertex of this triangle, grow a square outward.
#    The size of each square should be equal to the length of the opposite side of the triangle.
# 3. Continue growing squares from each vertex, increasing their size by the length of the opposite side each time.
# 4. Stop growing when no new pixels can be added to the grid.

def main(input_grid):
    # Find the three colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    assert len(colored_pixels) == 3

    # Sort the pixels by their x-coordinate
    pixels = sorted(colored_pixels, key=lambda p: p[0])
    
    # Extract coordinates and colors
    (x1, y1), (x2, y2), (x3, y3) = pixels
    color1, color2, color3 = input_grid[x1, y1], input_grid[x2, y2], input_grid[x3, y3]

    output_grid = np.full_like(input_grid, Color.BLACK)

    # Draw the initial triangle
    draw_line(output_grid, x1, y1, None, color1, (1, 0))
    draw_line(output_grid, x1, y1, None, color1, (0, 1))
    draw_line(output_grid, x2, y2, None, color2, (0, 1))
    draw_line(output_grid, x3, y3, None, color3, (1, 0))

    # Calculate side lengths
    side1 = abs(x2 - x1)
    side2 = abs(y3 - y1)
    hypotenuse = abs(x3 - x1)

    def draw_square(center_x, center_y, size, color):
        half_size = size // 2
        top_left_x = max(0, center_x - half_size)
        top_left_y = max(0, center_y - half_size)
        
        # Draw the square borders
        for i in range(size):
            if top_left_x + i < output_grid.shape[0]:
                if top_left_y < output_grid.shape[1]:
                    output_grid[top_left_x + i, top_left_y] = color
                if top_left_y + size - 1 < output_grid.shape[1]:
                    output_grid[top_left_x + i, top_left_y + size - 1] = color
            
            if top_left_y + i < output_grid.shape[1]:
                if top_left_x < output_grid.shape[0]:
                    output_grid[top_left_x, top_left_y + i] = color
                if top_left_x + size - 1 < output_grid.shape[0]:
                    output_grid[top_left_x + size - 1, top_left_y + i] = color

    # Grow squares from each vertex
    for multiplier in range(1, max(output_grid.shape)):
        draw_square(x1, y1, side1 * multiplier, color1)
        draw_square(x2, y2, hypotenuse * multiplier, color2)
        draw_square(x3, y3, side2 * multiplier, color3)
        
        # Check if we've filled the grid
        if np.all(output_grid != Color.BLACK):
            break

    return output_grid

def generate_input():
    grid_size = np.random.randint(20, 31)
    input_grid = np.full((grid_size, grid_size), Color.BLACK)

    # Choose three different colors
    colors = np.random.choice(list(Color.NOT_BLACK), 3, replace=False)

    # Generate the isosceles right triangle
    side_length = np.random.randint(3, grid_size // 2)
    start_x = np.random.randint(0, grid_size - side_length)
    start_y = np.random.randint(0, grid_size - side_length)

    input_grid[start_x, start_y] = colors[0]
    input_grid[start_x + side_length, start_y] = colors[1]
    input_grid[start_x, start_y + side_length] = colors[2]

    return input_grid