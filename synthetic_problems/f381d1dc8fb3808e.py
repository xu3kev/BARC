from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, flood fill, connecting same color, sliding objects

# description:
# The input grid is divided into rectangular cells by horizontal and vertical bars.
# Some cells contain colored objects.
# To make the output:
# 1. For each colored object, slide it horizontally or vertically until it touches another object of the same color or a divider.
# 2. After all slides are complete, flood fill the empty space between objects of the same color that are in the same row or column.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()
    
    # Find the color of the dividers
    divider_color = None
    for color in Color.ALL_COLORS:
        if np.any(np.all(input_grid == color, axis=0)) or np.any(np.all(input_grid == color, axis=1)):
            divider_color = color
            break
    assert divider_color is not None, "No divider color found"

    # Step 1: Slide objects
    for color in Color.ALL_COLORS:
        if color == divider_color or color == Color.BLACK:
            continue
        
        object_locations = np.argwhere(input_grid == color)
        for x, y in object_locations:
            # Try sliding horizontally
            for dx in [-1, 1]:
                new_x = x
                while 0 <= new_x + dx < input_grid.shape[0] and output_grid[new_x + dx, y] == Color.BLACK:
                    new_x += dx
                if new_x != x:
                    output_grid[new_x, y] = color
                    output_grid[x, y] = Color.BLACK
                    break
            
            # If didn't slide horizontally, try sliding vertically
            if new_x == x:
                for dy in [-1, 1]:
                    new_y = y
                    while 0 <= new_y + dy < input_grid.shape[1] and output_grid[x, new_y + dy] == Color.BLACK:
                        new_y += dy
                    if new_y != y:
                        output_grid[x, new_y] = color
                        output_grid[x, y] = Color.BLACK
                        break

    # Step 2: Flood fill between same colors
    for color in Color.ALL_COLORS:
        if color == divider_color or color == Color.BLACK:
            continue
        
        object_locations = np.argwhere(output_grid == color)
        for x1, y1 in object_locations:
            for x2, y2 in object_locations:
                if x1 == x2:  # Same row
                    start, end = min(y1, y2), max(y1, y2)
                    if np.all(output_grid[x1, start:end+1] == Color.BLACK) or \
                       np.all((output_grid[x1, start:end+1] == Color.BLACK) | (output_grid[x1, start:end+1] == color)):
                        output_grid[x1, start:end+1] = color
                elif y1 == y2:  # Same column
                    start, end = min(x1, x2), max(x1, x2)
                    if np.all(output_grid[start:end+1, y1] == Color.BLACK) or \
                       np.all((output_grid[start:end+1, y1] == Color.BLACK) | (output_grid[start:end+1, y1] == color)):
                        output_grid[start:end+1, y1] = color

    return output_grid

def generate_input() -> np.ndarray:
    grid_size = 32
    cell_size = 4

    # Create grid with dividers
    divider_color = random.choice(Color.NOT_BLACK)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    for x in range(0, grid_size, cell_size):
        grid[x, :] = divider_color
    for y in range(0, grid_size, cell_size):
        grid[:, y] = divider_color

    # Add colored objects
    colors = random.sample([c for c in Color.ALL_COLORS if c != divider_color and c != Color.BLACK], 3)
    for color in colors:
        for _ in range(random.randint(2, 4)):
            while True:
                x = random.randint(0, grid_size - 2)
                y = random.randint(0, grid_size - 2)
                if grid[x, y] == Color.BLACK and grid[x+1, y] == Color.BLACK and \
                   grid[x, y+1] == Color.BLACK and grid[x+1, y+1] == Color.BLACK:
                    grid[x:x+2, y:y+2] = color
                    break

    return grid