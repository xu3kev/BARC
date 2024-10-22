from common import *
import numpy as np
from typing import *

# concepts:
# rectangle detection

# description:
# In the input you will see a grid with random pixels on it (mostly blue pixels).
# To make the output, you should find the largest rectangular area (of height/width >= 2, i.e. not a line) of black cells and turn it into pink.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Enumerate all rectangular regions
    # 2. For each region, filter it out if it isn't all black
    # 3. Find the biggest region remaining by area
    # 4. Turn the biggest region into pink

    # 1. Enumerate all rectangular regions
    regions = { (x, y, w, h) for x in range(len(input_grid)) for y in range(len(input_grid[0])) for w in range(2, len(input_grid) - x + 1) for h in range(2, len(input_grid[0]) - y + 1) }

    # 2. For each region, filter it out if it isn't all black
    regions = { (x, y, w, h) for x, y, w, h in regions if np.all(input_grid[x:x+w, y:y+h] == Color.BLACK) }

    # 3. Find the biggest region remaining by area
    largest_region = max(regions, key=lambda region: region[2] * region[3])
    x, y, w, h = largest_region

    # 4. Turn the biggest region into pink
    output_grid = np.copy(input_grid)
    output_grid[x:x+w, y:y+h] = Color.PINK
    
    return output_grid

def generate_input() -> np.ndarray:
    # Generate the background grid with size of n x m.
    n, m = np.random.randint(20, 30), np.random.randint(3, 5)
    grid = np.zeros((n, m), dtype=int)

    # Random largest_rec_height scatter density of blue color pixels on the grid.
    randomly_scatter_points(grid, color=Color.BLUE, density=0.6)
    
    # Define random size for the pink rectangle, the rectangle should not be a line or point
    rectangle_width = max(2, random.randint(int(0.25 * n), int(0.45 * n)))
    rectangle_height = max(2, random.randint(int(0.5 * m), int(0.75 * m)))

    # The pink rectangle region are represented by color black
    rectangle = np.full((rectangle_width, rectangle_height), Color.BLACK)
    
    # Place the pink sprite at a random position in the grid
    x, y = random.randint(0, n - rectangle_width + 1), random.randint(0, m - rectangle_height + 1)
    blit_sprite(grid=grid, sprite=rectangle, x=x, y=y, background=Color.BLUE)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)