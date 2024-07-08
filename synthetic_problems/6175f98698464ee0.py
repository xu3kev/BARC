from common import *

import numpy as np
from typing import *

# concepts:
# diagonal movement, color matching, collision detection

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # find all green and red pixels
    green_positions = np.argwhere(input_grid == Color.GREEN)
    red_positions = np.argwhere(input_grid == Color.RED)
    
    # move each green pixel diagonally down-right until it hits another object or boundary
    for (x, y) in green_positions:
        dx, dy = x, y
        while True:
            if dx + 1 >= input_grid.shape[0] or dy + 1 >= input_grid.shape[1]:
                break  # hit boundary
            
            if output_grid[dx+1, dy+1] != Color.BLACK:
                break  # hit another object
            
            dx += 1
            dy += 1
        
        # check if it hits the red pixel and change it to yellow
        if (dx, dy) != (x, y) and output_grid[dx, dy] == Color.RED:
            output_grid[dx, dy] = Color.YELLOW
            output_grid[x, y] = Color.BLACK  # remove the initial green pixel
        else:
            output_grid[dx, dy] = Color.GREEN  # move original green pixel if no red found
    
    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)
    
    # place a few green pixels randomly
    num_green = np.random.randint(1, 10)
    for _ in range(num_green):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.GREEN
        
    # place a few red pixels randomly
    num_red = np.random.randint(1, 5)
    for _ in range(num_red):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED  # ensure overlap doesn't exist
        while grid[x, y] != Color.BLACK:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED
    
    return grid