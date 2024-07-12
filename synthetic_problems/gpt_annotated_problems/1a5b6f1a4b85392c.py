from common import *

import numpy as np
from typing import *

# concepts:
# counting, resizing, color, decomposition

# description:
# In the input, you will see a grid with colored pixels scattered around.
# To make the output:
# 1. Count the number of distinct colors (excluding black) in the input grid.
# 2. Enlarge every pixel in the input by a factor of the number of colors.
# 3. For each enlarged colored pixel:
#    a. If it's square (equal width and height), leave it as is.
#    b. If it's rectangular, decompose it into smaller squares:
#       - Fill the largest possible square in the top-left corner with the original color.
#       - Fill the remaining area with smaller squares of different colors, chosen from the input colors.
# 4. The background (black) pixels should remain black in the output.

def main(input_grid):
    # Count the number of distinct colors (excluding black)
    colors = set(input_grid.flatten()) - {Color.BLACK}
    num_colors = len(colors)

    # Magnify the pixels in input grid
    output_grid = np.repeat(np.repeat(input_grid, num_colors, axis=0), num_colors, axis=1)

    # Process each enlarged colored pixel
    height, width = output_grid.shape
    for y in range(0, height, num_colors):
        for x in range(0, width, num_colors):
            if output_grid[y, x] != Color.BLACK:
                original_color = output_grid[y, x]
                
                # Check if it's a square or rectangle
                if x + num_colors <= width and y + num_colors <= height:
                    if np.all(output_grid[y:y+num_colors, x:x+num_colors] == original_color):
                        # It's a square, leave it as is
                        continue
                
                # It's a rectangle, decompose it
                max_square_size = min(num_colors, width - x, height - y)
                
                # Fill the largest possible square with the original color
                output_grid[y:y+max_square_size, x:x+max_square_size] = original_color
                
                # Fill the remaining area with smaller squares of different colors
                remaining_colors = list(colors - {original_color})
                for i in range(max_square_size, num_colors):
                    if x + i < width:
                        output_grid[y:y+i, x+i] = np.random.choice(remaining_colors)
                    if y + i < height:
                        output_grid[y+i, x:x+i] = np.random.choice(remaining_colors)

    return output_grid

def generate_input():
    # Create a random-sized grid
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # Choose a random number of colors (2 to 5)
    num_colors = np.random.randint(2, 6)
    colors = random.sample(list(Color.NOT_BLACK), num_colors)

    # Randomly place colored pixels
    num_pixels = np.random.randint(num_colors, n*m//2)
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = np.random.choice(colors)

    return grid