from common import *
import numpy as np
from typing import *

# concepts:
# pattern extraction, color matching

# description:
# In the input you will see a grid with a central pattern corner by four pixels indicates a rectangle.
# To make the output, you should extract the central pattern by the rectangle indicates by four pixels 
# and change the color of the central pattern to match the corner squares.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract the central pattern by the four corner squares
    output_grid = np.copy(input_grid)
    for i in range(0, len(output_grid)):
        for j in range(0, len(output_grid[0])):
            # Check if the current cell is part of a corner square
            if output_grid[i, j] != Color.BLACK:
                x, y = i + 1, j + 1
                # Find the extent of the pattern by moving right and down
                while output_grid[x, j] == Color.BLACK:
                    x = x + 1
                while output_grid[i, y] == Color.BLACK:
                    y = y + 1
                # Extract the central pattern
                sub_matrix = output_grid[i + 1:x, j + 1:y]
                # Change the color of the central pattern to match the corner squares
                sub_matrix[sub_matrix != Color.BLACK] = output_grid[i, j]
                output_grid = sub_matrix
                return output_grid

def generate_input() -> np.ndarray:
    # Random generate the size of the pattern 
    n, m = random.randint(3, 10), random.randint(3, 10)

    # Get the color of the pattern and the corner squares
    available_colors = random.sample(Color.NOT_BLACK, 2)
    pattern_color, corner_color = available_colors[0], available_colors[1]
    
    # Generate a random pattern
    pattern = random_sprite(n, m, color_palette=[pattern_color], density=0.4)

    # Ensure there is space for the four corner squares
    enlarged_pattern = np.zeros((n + 2, m + 2), dtype=int)

    # Set four pixels in each corner to the corner color
    enlarged_pattern[0, 0] = corner_color
    enlarged_pattern[0, m + 1] = corner_color
    enlarged_pattern[n + 1, 0] = corner_color
    enlarged_pattern[n + 1, m + 1] = corner_color

    # Place the pattern in the center of the corner pixels
    enlarged_pattern = blit_sprite(grid=enlarged_pattern, sprite=pattern, x=1, y=1)
    
    # Create the grid and place the pattern in it
    grid_width, grid_height = random.randint(n + 2, 2 * n + 2), random.randint(m + 2, 2 * m + 2)
    grid = np.zeros((grid_width, grid_height), dtype=int)

    # Randomly place the pattern in the grid
    pos_x, pos_y = random.randint(0, grid_width - (n + 2)), random.randint(0, grid_height - (m + 2))
    grid = blit_sprite(grid=grid, sprite=enlarged_pattern, x=pos_x, y=pos_y)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
