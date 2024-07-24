from common import *

import numpy as np
import random
from typing import *

# concepts:
# reflection, symmetry detection, scaling

# description:
# In the input, you will see a grid with a pattern reflected around a central axis. 
# Your task is to identify the axis of reflection and scale the pattern by a factor of 2 along both dimensions, maintaining the reflection around the same axis.

def main(input_grid):
    output_grid = np.copy(input_grid)  # Start with a copy of the input grid

    # Identify the axis of reflection, which can be either vertical or horizontal
    height, width = input_grid.shape
    vertical_reflection = np.array_equal(input_grid[:, :width//2], np.flip(input_grid[:, width//2:], 1))
    horizontal_reflection = np.array_equal(input_grid[:height//2, :], np.flip(input_grid[height//2:, :], 0))

    if vertical_reflection:
        # Extract the left half and scale it
        left_half = input_grid[:, :width//2]
        scaled_left_half = np.kron(left_half, np.ones((2,2), dtype=int))  # Scale by a factor of 2
        
        # Create the new reflected part
        scaled_right_half = np.flip(scaled_left_half, 1)

        # Combine them together with scaling
        output_grid = np.zeros((height*2, width*2), dtype=int)
        output_grid[:height*2, :width*2//2] = scaled_left_half
        output_grid[:height*2, width*2//2:] = scaled_right_half

    elif horizontal_reflection:
        # Extract the top half and scale it
        top_half = input_grid[:height//2, :]
        scaled_top_half = np.kron(top_half, np.ones((2,2), dtype=int))
        
        # Create the new reflected part
        scaled_bottom_half = np.flip(scaled_top_half, 0)

        # Combine them together with scaling
        output_grid = np.zeros((height*2, width*2), dtype=int)
        output_grid[:height*2//2, :width*2] = scaled_top_half
        output_grid[height*2//2:, :width*2] = scaled_bottom_half

    return output_grid

def generate_input():
    # Create a random size for grid within range 5 to 10 for both dimensions
    height = random.randint(5, 10)
    width = random.randint(5, 10)
    
    # Create a grid filled with a base color (black)
    grid = np.zeros((height, width), dtype=int)
    
    # Random select horizontal_reflection or vertical_reflection
    reflection_type = random.choice(["vertical", "horizontal"])
    
    # Create a random pattern on half of the grid
    color_palette = list(Color.NOT_BLACK)
    pattern_half = random_sprite(height//2 if reflection_type == "horizontal" else height, width//2 if reflection_type == "vertical" else width, color_palette=color_palette)
    
    if reflection_type == "vertical":
        # Fill in the left half with the pattern
        grid[:, :width//2] = pattern_half
        
        # Reflect to the right half
        grid[:, width//2:] = np.flip(pattern_half, 1)
    
    elif reflection_type == "horizontal":
        # Fill in the top half with the pattern
        grid[:height//2, :] = pattern_half
        
        # Reflect to the bottom half
        grid[height//2:, :] = np.flip(pattern_half, 0)

    return grid