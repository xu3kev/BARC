from common import *

import numpy as np
from typing import *

# concepts:
# objects, color mapping, connecting same color

# description:
# The input grid contains colored shapes scattered across the grid.
# To make the output, connect shapes of the same color using vertical or horizontal lines passing through black cells only.


def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()
    
    shape_positions = {}
    
    # Determine positions of all the shapes
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]
            if color != Color.BLACK and color not in shape_positions:
                shape_positions[color] = []
            if color != Color.BLACK:
                shape_positions[color].append((x, y))
    
    # Connect shapes of the same color with a vertical or horizontal line
    for color, positions in shape_positions.items():
        if len(positions) < 2:
            continue
            
        # We assume the first two positions for simplicity, but this could be expanded
        (x1, y1), (x2, y2) = positions[:2]
        
        if x1 == x2:  # Same row
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if output_grid[x1][y] == Color.BLACK:
                    output_grid[x1][y] = color
        elif y1 == y2:  # Same column
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if output_grid[x][y1] == Color.BLACK:
                    output_grid[x][y1] = color
        else:
            # Connect based on directionality preference horizontal first, then vertical
            if y1 != y2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if output_grid[x1][y] == Color.BLACK:
                        output_grid[x1][y] = color
            if x1 != x2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    if output_grid[x][y2] == Color.BLACK:
                        output_grid[x][y2] = color

    return output_grid


def generate_input() -> np.ndarray:
    grid_size = 20
    num_shapes = 6
    possible_colors = list(Color.NOT_BLACK)
    
    grid = np.full((grid_size, grid_size), Color.BLACK, dtype=int)

    used_positions = set()

    for _ in range(num_shapes):
        color = random.choice(possible_colors)
        shape = random_sprite(n=[1, 2, 3], m=[1, 2, 3], color_palette=[color])
        
        # Generate two positions for this shape
        for _ in range(2):
            while True:
                x, y = random_free_location_for_sprite(grid, shape)
                if (x, y) not in used_positions:
                    break
            used_positions.add((x, y))
            blit_sprite(grid, shape, x, y)

    return grid