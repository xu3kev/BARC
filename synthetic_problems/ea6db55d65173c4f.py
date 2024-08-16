from common import *

import numpy as np
from typing import *

# concepts:
# rotational symmetry, square sections

# description:
# In the input grid, you will see colored pixels arranged in different sections.
# Your task is to generate an output grid that applies a 90-degree clockwise rotation to each section.
# The section is defined as a square subgrid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Determine the size of the grid and the section size
    n, m = input_grid.shape
    section_size = int(np.sqrt(n * m // (1)))  # assuming sections are perfect squares
    # Create the output grid
    output_grid = np.zeros_like(input_grid)
    
    # Create the rotated sections
    for i in range(0, n, section_size):
        for j in range(0, m, section_size):
            section = input_grid[i:i+section_size, j:j+section_size]
            rotated_section = np.rot90(section, -1)
            output_grid[i:i+section_size, j:j+section_size] = rotated_section
    
    return output_grid

def generate_input() -> np.ndarray:
    # Set the section size and the grid size
    section_size = np.random.choice([2, 3, 4])
    n_sections = np.random.randint(2, 5)
    grid_size = section_size * n_sections
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Fill each section with random colors
    for i in range(0, grid_size, section_size):
        for j in range(0, grid_size, section_size):
            section = random_sprite(section_size, section_size, color_palette=list(Color.NOT_BLACK), symmetry=None)
            blit(grid, section, x=i, y=j)
    
    return grid