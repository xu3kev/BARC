from common import *

import numpy as np
from typing import *

# concepts:
# lines, connecting colors, repeating pattern

# description:
# In the input grid, you will see an all black grid with three dots of the same color in a line at arbitrary angles, 
# but equally spaced apart from each other. The three points will always form one of the angles in a regular octagon.
# The objective is to produce concentric octagons with units found by:
# 1. connecting the outer two points, creating the next largest regular octagon centered on the middle point.
# 2. producing larger concentric octagons.

def main(input_grid):
    # Plan:
    # 1. Identify the three points
    # 2. Calculate distance from the center point to the outer points
    # 3. Use trigonometric functions to create concentric octagons starting from the distance between the center point and the outer points.
    # 4. Draw the octagons until they would extend beyond the grid.

    # Get the dot positions
    pixel_xs, pixel_ys = np.where(input_grid != Color.BLACK)
    pixel_locations = list(zip(pixel_xs, pixel_ys))
    assert len(pixel_locations) == 3
    
    # sort by distance
    central_dot = sorted(pixel_locations, key=lambda l: l[0]**2 + l[1]**2)[1]
    dist = int(np.linalg.norm(np.subtract(pixel_locations[0], pixel_locations[1])))

    output_grid = input_grid.copy()

    def draw_octagon(center, radius, color):
        cx, cy = center
        for angle in range(0, 360, 45):
            x = cx + int(radius * np.cos(np.radians(angle)))
            y = cy + int(radius * np.sin(np.radians(angle)))
            if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                output_grid[x, y] = color

    color = input_grid[pixel_locations[0][0], pixel_locations[0][1]]
    multiplier = 1
    while True:
        draw_octagon(central_dot, dist * multiplier, color)
        if np.any(output_grid != input_grid):
            multiplier += 1
            input_grid = output_grid.copy()
        else:
            break

    return output_grid

def generate_input():
    input_grid = np.full((20, 20), Color.BLACK)
    distance = np.random.randint(3, 5)
    color = np.random.choice(Color.NOT_BLACK)
    central_x = np.random.randint(distance, 20 - distance)
    central_y = np.random.randint(distance, 20 - distance)
    angle = np.random.choice([0, 45, 90, 135])

    input_grid[central_x, central_y] = color
    input_grid[central_x + int(distance * np.cos(np.radians(angle))), central_y + int(distance * np.sin(np.radians(angle)))] = color
    input_grid[central_x - int(distance * np.cos(np.radians(angle))), central_y - int(distance * np.sin(np.radians(angle)))] = color
    
    return input_grid