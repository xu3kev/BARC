from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, alignment, scaling

# description:
# In the input, you will see a rectangular grid with two colored pixels: one red and one blue.
# To make the output:
# 1. Draw a yellow line from the red pixel to the blue pixel.
# 2. Find the midpoint of this line.
# 3. Draw a green line perpendicular to the yellow line, centered at the midpoint.
#    The length of the green line should be half the length of the yellow line.
# 4. The green line forms two endpoints. At each of these endpoints, draw a pink circle.
#    The diameter of each circle should be 1/4 the length of the yellow line.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find red and blue pixels
    red_coords = np.argwhere(input_grid == Color.RED)[0]
    blue_coords = np.argwhere(input_grid == Color.BLUE)[0]
    
    # Calculate direction and length of yellow line
    direction = blue_coords - red_coords
    length = int(np.linalg.norm(direction))
    unit_direction = direction / length
    
    # Draw yellow line
    for i in range(length + 1):
        x, y = np.round(red_coords + i * unit_direction).astype(int)
        output_grid[x, y] = Color.YELLOW
    
    # Find midpoint
    midpoint = (red_coords + blue_coords) // 2
    
    # Calculate perpendicular direction
    perp_direction = np.array([-direction[1], direction[0]])
    perp_unit_direction = perp_direction / np.linalg.norm(perp_direction)
    
    # Draw green perpendicular line
    green_length = length // 2
    for i in range(-green_length // 2, green_length // 2 + 1):
        x, y = np.round(midpoint + i * perp_unit_direction).astype(int)
        if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
            output_grid[x, y] = Color.GREEN
    
    # Draw pink circles at endpoints of green line
    circle_radius = length // 8
    for endpoint in [midpoint + (green_length // 2) * perp_unit_direction,
                     midpoint - (green_length // 2) * perp_unit_direction]:
        x, y = np.round(endpoint).astype(int)
        for dx in range(-circle_radius, circle_radius + 1):
            for dy in range(-circle_radius, circle_radius + 1):
                if dx**2 + dy**2 <= circle_radius**2:
                    px, py = x + dx, y + dy
                    if 0 <= px < output_grid.shape[0] and 0 <= py < output_grid.shape[1]:
                        output_grid[px, py] = Color.PINK
    
    return output_grid

def generate_input():
    n = np.random.randint(20, 30)
    m = np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK, dtype=int)
    
    # Place red pixel
    red_x, red_y = np.random.randint(0, n), np.random.randint(0, m)
    grid[red_x, red_y] = Color.RED
    
    # Place blue pixel (ensuring it's not too close to the red pixel)
    while True:
        blue_x, blue_y = np.random.randint(0, n), np.random.randint(0, m)
        if abs(blue_x - red_x) + abs(blue_y - red_y) > max(n, m) // 3:
            grid[blue_x, blue_y] = Color.BLUE
            break
    
    return grid