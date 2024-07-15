from common import *

import numpy as np
from typing import *

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # find the coordinates of all blue pixels in the grid
    blue_coords = np.argwhere(input_grid == Color.BLUE)
    
    # find the coordinates of all green pixels in the grid
    green_coords = np.argwhere(input_grid == Color.GREEN)
    
    if blue_coords.size > 0:
        # Define the leftmost and rightmost blue pixel coordinates
        leftmost_blue = blue_coords[np.argmin(blue_coords[:, 1])]
        rightmost_blue = blue_coords[np.argmax(blue_coords[:, 1])]
        
        # Draw horizontal blue line
        draw_line(output_grid, leftmost_blue[0], leftmost_blue[1], length=None, color=Color.BLUE, direction=(0, 1))

    if green_coords.size > 0:
        # Define the topmost and bottommost green pixel coordinates
        topmost_green = green_coords[np.argmin(green_coords[:, 0])]
        bottommost_green = green_coords[np.argmax(green_coords[:, 0])]
        
        # Draw vertical green line
        draw_line(output_grid, topmost_green[0], topmost_green[1], length=None, color=Color.GREEN, direction=(1, 0))

    # If a blue and green line intersect, color the intersection purple
    if blue_coords.size > 0 and green_coords.size > 0:
        blue_line_coords = np.argwhere(output_grid == Color.BLUE)
        green_line_coords = np.argwhere(output_grid == Color.GREEN)
        
        # Find intersection points
        intersection_coords = [tuple(x) for x in blue_line_coords if any((x == y).all() for y in green_line_coords)]
        
        for (x, y) in intersection_coords:
            output_grid[x, y] = Color.PURPLE

    return output_grid

def generate_input():
    # Make a random sized grid
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # Place a random number of blue and green pixels
    num_blue = np.random.randint(1, min(n, m) + 1)
    num_green = np.random.randint(1, min(n, m) + 1)

    blue_sprite = np.array([Color.BLUE]).reshape(1, 1)
    for _ in range(num_blue):
        x, y = random_free_location_for_sprite(grid, blue_sprite, padding=0)
        blit_sprite(grid, blue_sprite, x, y)

    green_sprite = np.array([Color.GREEN]).reshape(1, 1)
    for _ in range(num_green):
        x, y = random_free_location_for_sprite(grid, green_sprite, padding=0)
        blit_sprite(grid, green_sprite, x, y)

    return grid