from common import *
import numpy as np

# concepts:
# reflection, symmetry

# description:
# In the input, you will see a rectangular pattern in the top-left quadrant 
# of the grid. This pattern is symmetrical around both its vertical and horizontal axes.
# To make the output, reflect this quadrant vertically to right quadrants 
# and horizontally downwards to fill the entire grid.

def main(input_grid):
    # Get the dimensions of the input grid
    n, m = input_grid.shape
    
    # Reflect horizontally to complete top half
    top_half = np.hstack((input_grid[:, :m // 2], input_grid[:, :m // 2][:, ::-1]))
    
    # Reflect vertically to complete the entire grid
    output_grid = np.vstack((top_half, top_half[::-1, :]))
    
    return output_grid

def generate_input():
    # Define the dimensions for the main quadrant (should be even to simplify the reflections)
    row_dim = np.random.randint(4, 6) * 2
    col_dim = np.random.randint(4, 6) * 2
    
    # Generate half patterns
    main_quarter = random_sprite(row_dim // 2, col_dim // 2, color_palette=Color.NOT_BLACK, density=0.7)
    
    # Combine quarters to form a symmetrical full quadrant
    half_horizontal = np.hstack((main_quarter, main_quarter[:, ::-1]))
    full_pattern = np.vstack((half_horizontal, half_horizontal[::-1, :]))
    
    # Create a grid of double size to place the quarter pattern
    full_grid = np.zeros((row_dim, col_dim), dtype=int)

    # Place the full pattern in the top-left quadrant of this grid
    full_grid[:row_dim // 2, :col_dim // 2] = main_quarter

    return full_grid