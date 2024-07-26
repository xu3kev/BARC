from common import *

import numpy as np
from typing import *

# concepts:
# repetition, connecting colors, rotation

# description:
# In the input grid, three colored pixels of the same color are positioned to form a triangle with a base parallel to either row or column.
# To create the output grid, identify the triangle formed by the colored pixels. 
# Rotate the triangle 90 degrees counterclockwise around its centroid.
# Then repeat this rotation two more times to create three additional triangles, making a full 360-degree rotation in total.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Find the three pixels of the same color in the input grid
    # 2. Calculate the centroid of the triangle formed by these pixels
    # 3. Compute the 90-degree rotation of the triangle around its centroid
    # 4. Draw the rotated triangle on the output grid, repeat rotation to form full 360 degrees rotation

    def rotate_point(cx, cy, x, y, angle):
        radians = np.deg2rad(angle)
        cos_theta = np.cos(radians)
        sin_theta = np.sin(radians)
        nx = cos_theta * (x - cx) - sin_theta * (y - cy) + cx
        ny = sin_theta * (x - cx) + cos_theta * (y - cy) + cy
        return round(nx), round(ny)

    output_grid = np.copy(input_grid)
    # Find the color and positions of the triangle pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    unique_colors = set([input_grid[x, y] for x, y in colored_pixels])
    triangle_color = None
    for color in unique_colors:
        color_positions = [(x, y) for x, y in colored_pixels if input_grid[x, y] == color]
        if len(color_positions) == 3:
            triangle_color = color
            break

    # Calculate the centroid of the triangle
    x_coords, y_coords = zip(*color_positions)
    centroid_x = sum(x_coords) / 3
    centroid_y = sum(y_coords) / 3

    # Create rotated versions of the triangle
    for i in range(1, 4):
        angle = i * 90
        for x, y in color_positions:
            nx, ny = rotate_point(centroid_x, centroid_y, x, y, angle)
            if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                output_grid[nx, ny] = triangle_color

    return output_grid


def generate_input() -> np.ndarray:
    # Create a black grid
    n, m = 15, 15
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Select a random color for the triangle
    triangle_color = np.random.choice(Color.NOT_BLACK)

    # Generate a random base for the triangle
    base_orientation = np.random.choice(["horizontal", "vertical"])
    base_length = np.random.randint(3, 6)
    
    if base_orientation == "horizontal":
        base_coords = (np.random.randint(base_length - 1, n - base_length + 1), np.random.randint(base_length - 1, m))
        color_positions = [
            (base_coords[0], base_coords[1]),
            (base_coords[0] - 1, base_coords[1] - 1),
            (base_coords[0] + 1, base_coords[1] - 1)
        ]
    else:  # base_orientation == "vertical"
        base_coords = (np.random.randint(base_length - 1, n), np.random.randint(base_length - 1, m - base_length + 1))
        color_positions = [
            (base_coords[0], base_coords[1]),
            (base_coords[0] - 1, base_coords[1] + 1),
            (base_coords[0] - 1, base_coords[1] - 1)
        ]

    # Place the triangle pixels in the grid
    for x, y in color_positions:
        grid[x, y] = triangle_color

    return grid