from common import *
import numpy as np
from typing import *

# concepts:
# pattern extraction, color matching

# description:
# In the input you will see a grid with a central pattern with four differently-colored pixels at the corners.
# To make the output, you should extract the central pattern (removing the differently-colored corners), 
# and change the color of the central pattern to match the corner pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract the central pattern by the four corner squares
    output_grid = np.copy(input_grid)

    # Crop the pattern out
    output_grid = crop(grid=output_grid)

    # Get the color of the corner squares
    corner_color = output_grid[0, 0]

    # Change the color of the central pattern to match the corner squares
    output_grid[output_grid != Color.BLACK] = corner_color

    # Remove the one pixel border around the central pattern
    output_grid = output_grid[1:-1, 1:-1]
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
