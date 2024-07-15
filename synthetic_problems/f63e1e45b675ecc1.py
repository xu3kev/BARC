from common import *

import numpy as np
from typing import *

# concepts:
# connectivity, objects, symmetry

# description:
# In the input image, you will see several blue pixels forming a path, and two 3x3 red squares on a black background.
# The blue path may or may not connect the two red squares.
# If the blue path connects the red squares, output a 3x3 grid with rotational symmetry using only blue pixels.
# If the blue path does not connect the red squares, output a 3x3 grid with mirror symmetry using only blue pixels.

def main(input_grid):
    # Create output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Get just the red squares
    red_squares = np.zeros_like(input_grid)
    red_squares[input_grid == Color.RED] = Color.RED

    # Find all connected components
    connected_components = find_connected_components(input_grid, connectivity=4, monochromatic=False)

    # Check if any connected component contains both red squares
    red_squares_connected = any(np.all(component[red_squares == Color.RED] == Color.RED) for component in connected_components)

    if red_squares_connected:
        # Create a 3x3 grid with rotational symmetry
        output_grid[1, 1] = Color.BLUE  # Center
        output_grid[0, 0] = Color.BLUE  # Corners
        output_grid[0, 2] = Color.BLUE
        output_grid[2, 0] = Color.BLUE
        output_grid[2, 2] = Color.BLUE
    else:
        # Create a 3x3 grid with mirror symmetry
        output_grid[1, :] = Color.BLUE  # Middle row
        output_grid[0, 1] = Color.BLUE  # Top and bottom center
        output_grid[2, 1] = Color.BLUE

    return output_grid

def generate_input():
    # Make a black grid as background
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Make a 3x3 red square sprite
    red_square_sprite = np.full((3, 3), Color.RED, dtype=int)

    # Place two red square sprites at random locations
    x1, y1 = random_free_location_for_sprite(grid, red_square_sprite, padding=1)
    blit_sprite(grid, red_square_sprite, x1, y1)
    x2, y2 = random_free_location_for_sprite(grid, red_square_sprite, padding=1)
    blit_sprite(grid, red_square_sprite, x2, y2)

    # Generate a blue path
    path_connected = np.random.choice([True, False])
    if path_connected:
        # Create a connected path between the two red squares
        start = (x1 + 1, y1 + 1)
        end = (x2 + 1, y2 + 1)
        path = []
        current = start
        while current != end:
            path.append(current)
            if current[0] < end[0]:
                current = (current[0] + 1, current[1])
            elif current[0] > end[0]:
                current = (current[0] - 1, current[1])
            elif current[1] < end[1]:
                current = (current[0], current[1] + 1)
            else:
                current = (current[0], current[1] - 1)
        path.append(end)
        
        for x, y in path:
            if grid[x, y] == Color.BLACK:
                grid[x, y] = Color.BLUE
    else:
        # Create two separate blue paths
        for _ in range(2):
            path_length = np.random.randint(5, 10)
            x, y = random_free_location_for_sprite(grid, np.array([[Color.BLUE]]), padding=1)
            for _ in range(path_length):
                if grid[x, y] == Color.BLACK:
                    grid[x, y] = Color.BLUE
                dx, dy = np.random.choice([-1, 0, 1], size=2)
                x, y = np.clip(x + dx, 0, n - 1), np.clip(y + dy, 0, m - 1)

    return grid