from common import *

import numpy as np
from typing import *

# concepts:
# objects, occlusion, alignment

# description:
# In the input you have four regions separated by green vertical bars. Each region is rectangular, arranged horizontally:
# left (blue pattern), center-left (red pattern), center-right (yellow pattern), and right (maroon pattern).
# To make the output, align the vertical heights of all patterns to match the height of the blue pattern.
# Then overlay the regions sequentially (right to left) with colors as follows:
# maroon -> yellow -> red -> blue.

def main(input_grid):
    # Find the vertical green bars that separate the sections
    green_bars = np.where(input_grid == Color.GREEN)

    # Get unique x-coordinates of the green bars
    green_bars_x = np.unique(green_bars[0])

    # Define start and end indices for each section
    start_idx = np.insert(green_bars_x + 1, 0, 0)
    end_idx = np.append(green_bars_x, input_grid.shape[0])

    # Extract each pattern region
    blue_pattern = input_grid[start_idx[0]:end_idx[0], :]
    red_pattern = input_grid[start_idx[1]:end_idx[1], :]
    yellow_pattern = input_grid[start_idx[2]:end_idx[2], :]
    maroon_pattern = input_grid[start_idx[3]:end_idx[3], :]

    # Determine the output grid height (same as blue pattern)
    output_height = blue_pattern.shape[0]

    # Initialize output grid with the same shape as input grid but only the height of blue pattern
    output_grid = np.full((output_height, input_grid.shape[1]), Color.BLACK, dtype=int)

    # Create a function to align vertically any pattern height with that of blue pattern height
    def align_pattern_height(pattern, target_height):
        aligned_pattern = np.full((target_height, pattern.shape[1]), Color.BLACK, dtype=int)
        min_height = min(target_height, pattern.shape[0])
        aligned_pattern[:min_height, :] = pattern[:min_height, :]
        return aligned_pattern

    # Align patterns
    red_pattern = align_pattern_height(red_pattern, output_height)
    yellow_pattern = align_pattern_height(yellow_pattern, output_height)
    maroon_pattern = align_pattern_height(maroon_pattern, output_height)

    # Overlay patterns: maroon -> yellow -> red -> blue
    output_grid = np.where(maroon_pattern != Color.BLACK, maroon_pattern, output_grid)
    output_grid = np.where(yellow_pattern != Color.BLACK, yellow_pattern, output_grid)
    output_grid = np.where(red_pattern != Color.BLACK, red_pattern, output_grid)
    output_grid = np.where(blue_pattern != Color.BLACK, blue_pattern, output_grid)

    return output_grid

def generate_input():
    # Define a green divider for sectional splits
    green_divider = np.full((1, 4), Color.GREEN, dtype=int)

    # Generate random sections with scattered pixels of respective colors
    def generate_section(color):
        section = np.zeros((4, 4), dtype=int)
        for _ in range(12):
            x, y = np.random.randint(section.shape[1]), np.random.randint(section.shape[0])
            section[x, y] = color
        return section

    # Generate each colored section
    blue_section = generate_section(Color.BLUE)
    red_section = generate_section(Color.RED)
    yellow_section = generate_section(Color.YELLOW)
    maroon_section = generate_section(Color.MAROON)

    # Concatenate these sections with green dividers
    grid = np.vstack([blue_section, green_divider, red_section, green_divider, yellow_section, green_divider, maroon_section])

    return grid