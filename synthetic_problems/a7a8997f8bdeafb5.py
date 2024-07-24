from common import *
import numpy as np
from typing import *

def main(input_grid):

    # Find all the 2x2 blocks
    blocks = []
    for x in range(input_grid.shape[0]-1):
        for y in range(input_grid.shape[1]-1):
            block = input_grid[x:x+2, y:y+2]
            if np.any(block != Color.BLACK):
                blocks.append(block)

    # Create the output grid
    output_grid = np.zeros_like(input_grid)

    # Place obstacles as they were in the input
    obstacles = np.argwhere(input_grid == Color.BLACK)
    for obstacle in obstacles:
        output_grid[obstacle[0], obstacle[1]] = Color.BLACK
    
    # Align blocks into two rows in the output grid
    row1_y = 0
    row2_y = 2
    for i, block in enumerate(blocks):
        if i < len(blocks) // 2:
            x = i * 2
            y = row1_y
        else:
            x = (i - len(blocks) // 2) * 2
            y = row2_y

        # Fill the obscured parts before placing on the output grid
        for dx in range(2):
            for dy in range(2):
                block_x = x + dx
                block_y = y + dy
                if block_x < output_grid.shape[0] and block_y < output_grid.shape[1]:
                    if block[dx, dy] != Color.BLACK:
                        output_grid[block_x, block_y] = block[dx, dy]

    return output_grid

def generate_input():
    # Create random grid size from 10x10 to 15x15
    n = np.random.randint(10, 16)
    m = np.random.randint(10, 16)
    grid = np.zeros((n, m), dtype=int)

    # Generate a few 2x2 colored blocks
    colors = random.sample(Color.ALL_COLORS, len(Color.ALL_COLORS))
    num_blocks = random.randint(4, 8)
    blocks = [random_sprite(2, 2, color_palette=colors[i:i+1]) for i in range(num_blocks)]

    # Place blocks randomly on the grid
    for block in blocks:
        x, y = random_free_location_for_sprite(grid, block, padding=1, padding_connectivity=4)
        blit_sprite(grid, block, x, y)

    # Add some random obstacles (single Black pixels)
    for _ in range(random.randint(5, 10)):
        x, y = random_free_location_for_sprite(grid, np.array([[Color.BLACK]]))
        grid[x, y] = Color.BLACK  

    return grid