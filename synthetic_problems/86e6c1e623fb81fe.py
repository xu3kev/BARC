from common import *
import numpy as np
import random

# concepts:
# patterns, reflection, rotation, color

# description:
# The input grid consists of 4 color patterns (one in each quadrant). Each pattern is rotated randomly.
# The output grid has all the quadrants adjusted such that the patterns are directed towards the central point of the grid.

def main(input_grid):
    # Get the dimensions of the grid
    height, width = input_grid.shape
    half_height, half_width = height // 2, width // 2

    # Extract quadrants
    top_left = input_grid[:half_height, :half_width]
    top_right = input_grid[:half_height, half_width:]
    bottom_left = input_grid[half_height:, :half_width]
    bottom_right = input_grid[half_height:, half_width:]

    # Rotate quadrants to align towards the center
    top_right = np.rot90(top_right, k=3)  # Rotate 90 degrees counter-clockwise
    bottom_right = np.rot90(bottom_right, k=2)  # Rotate 180 degrees
    bottom_left = np.rot90(bottom_left, k=1)  # Rotate 90 degrees clockwise

    # Reconstruct the output grid
    output_grid = np.zeros_like(input_grid)
    output_grid[:half_height, :half_width] = top_left
    output_grid[:half_height, half_width:] = top_right
    output_grid[half_height:, :half_width] = bottom_left
    output_grid[half_height:, half_width:] = bottom_right

    return output_grid

def generate_input():
    # Define the size of the grid
    n, m = random.choice([(6, 6), (8, 8), (10, 10)])  # ensuring the grid is even-sized
    half_n, half_m = n // 2, m // 2

    # Create the full grid
    input_grid = np.zeros((n, m), dtype=int)

    # Generate a random pattern for each quadrant
    colors = list(Color.NOT_BLACK)
    for quadrant in [(0, 0, half_n, half_m), (0, half_m, half_n, m), (half_n, 0, n, half_m), (half_n, half_m, n, m)]:
        x1, y1, x2, y2 = quadrant
        pattern = random_sprite(x2-x1, y2-y1, density=1, symmetry="not_symmetric", color_palette=random.sample(colors, 3))
        pattern = np.rot90(pattern, k=random.randint(0, 3))
        input_grid[x1:x2, y1:y2] = pattern

    return input_grid