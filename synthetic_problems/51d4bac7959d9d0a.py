from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, direction, lines, growing

# description:
# In the input, you will see a black grid with green pixels scattered along one edge and blue pixels scattered along an edge perpendicular to the green one.
# To make the output:
# 1. Make the green pixels grow into lines perpendicular to their starting edge, extending to the opposite edge.
# 2. Make the blue pixels act as magnets, attracting the nearest part of each green line.
# 3. When a green line is attracted to a blue pixel, it bends at a right angle towards the blue pixel.
# 4. If a green line reaches a blue pixel, it stops growing.
# 5. If green lines intersect, they merge and continue growing as a single line.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Determine the direction of growth for green lines
    if Color.GREEN in output_grid[:, 0]:  # Green on left edge
        green_direction = (0, 1)  # Grow right
    elif Color.GREEN in output_grid[:, -1]:  # Green on right edge
        green_direction = (0, -1)  # Grow left
    elif Color.GREEN in output_grid[0, :]:  # Green on top edge
        green_direction = (1, 0)  # Grow down
    else:  # Green on bottom edge
        green_direction = (-1, 0)  # Grow up

    # Find green and blue pixel positions
    green_pixels = np.argwhere(output_grid == Color.GREEN)
    blue_pixels = np.argwhere(output_grid == Color.BLUE)

    # Grow green lines
    while len(green_pixels) > 0:
        new_green_pixels = []
        for x, y in green_pixels:
            # Find nearest blue pixel
            distances = np.sum((blue_pixels - [x, y])**2, axis=1)
            nearest_blue = blue_pixels[np.argmin(distances)]

            # Determine growth direction
            if np.array_equal([x, y], nearest_blue):
                continue  # Stop growing if reached blue pixel
            elif x == nearest_blue[0] or y == nearest_blue[1]:
                dx, dy = np.sign(nearest_blue - [x, y])
            else:
                dx, dy = green_direction

            # Grow in the determined direction
            new_x, new_y = x + dx, y + dy

            # Check if within grid and not hitting blue pixel
            if 0 <= new_x < height and 0 <= new_y < width and output_grid[new_x, new_y] != Color.BLUE:
                output_grid[new_x, new_y] = Color.GREEN
                new_green_pixels.append((new_x, new_y))

        # Merge intersecting green lines
        green_pixels = list(set(new_green_pixels))

    return output_grid

def generate_input():
    # Create a black grid
    height, width = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.full((height, width), Color.BLACK)

    # Decide which edges to place green and blue pixels
    edges = ['top', 'bottom', 'left', 'right']
    green_edge, blue_edge = np.random.choice(edges, 2, replace=False)

    # Place green pixels
    if green_edge in ['top', 'bottom']:
        y = 0 if green_edge == 'top' else height - 1
        for x in np.random.choice(range(width), np.random.randint(3, 6), replace=False):
            grid[y, x] = Color.GREEN
    else:
        x = 0 if green_edge == 'left' else width - 1
        for y in np.random.choice(range(height), np.random.randint(3, 6), replace=False):
            grid[y, x] = Color.GREEN

    # Place blue pixels
    if blue_edge in ['top', 'bottom']:
        y = 0 if blue_edge == 'top' else height - 1
        for x in np.random.choice(range(width), np.random.randint(3, 6), replace=False):
            grid[y, x] = Color.BLUE
    else:
        x = 0 if blue_edge == 'left' else width - 1
        for y in np.random.choice(range(height), np.random.randint(3, 6), replace=False):
            grid[y, x] = Color.BLUE

    return grid