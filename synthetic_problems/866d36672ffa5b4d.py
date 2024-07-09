from common import *

import numpy as np
from typing import *

# concepts:
# counting, connecting colors, repeating pattern

# description:
# In the input, you will see a grid with multiple 2x2 squares of various colors and some single-pixel dots of various colors.
# To create the output:
# 1. Count the number of 2x2 squares for each color.
# 2. For each color with at least one 2x2 square, create a horizontal line in the output grid.
# 3. The length of each line should be equal to the count of 2x2 squares of that color.
# 4. The lines should be ordered from top to bottom based on the count (longest line at the top).
# 5. There should be one empty row between each colored line.
# The output grid should be just large enough to contain all the lines with the required spacing.

def main(input_grid):
    # Count 2x2 squares of each color
    color_counts = {}
    for x in range(input_grid.shape[0] - 1):
        for y in range(input_grid.shape[1] - 1):
            color = input_grid[x, y]
            if color != Color.BLACK and np.all(input_grid[x:x+2, y:y+2] == color):
                color_counts[color] = color_counts.get(color, 0) + 1
    
    # Sort colors by count (descending order)
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate output grid size
    max_count = sorted_colors[0][1] if sorted_colors else 0
    output_height = len(sorted_colors) * 2 - 1 if sorted_colors else 0
    output_grid = np.zeros((output_height, max_count), dtype=int)
    
    # Fill output grid
    for i, (color, count) in enumerate(sorted_colors):
        output_grid[i*2, :count] = color
    
    return output_grid

def generate_input():
    # Create a 12x12 black background grid
    grid = np.zeros((12, 12), dtype=int)
    
    # List of colors to use (excluding black)
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)
    
    # Create 2x2 squares
    square = np.ones((2, 2), dtype=int)
    for color in colors[:np.random.randint(3, 6)]:  # Use 3-5 colors
        for _ in range(np.random.randint(1, 5)):  # 1-4 squares per color
            x, y = random_free_location_for_sprite(grid, square, padding=1)
            blit_sprite(grid, square * color, x, y)
    
    # Add single-pixel dots
    for _ in range(np.random.randint(5, 10)):
        color = np.random.choice(colors)
        x, y = random_free_location_for_sprite(grid, np.array([[1]]))
        grid[x, y] = color
    
    return grid