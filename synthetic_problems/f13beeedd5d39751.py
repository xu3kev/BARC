from common import *

import numpy as np
from typing import *

# concepts:
# lines, repeating pattern, direction, topology

# description:
# In the input grid, you will see various colored pixels scattered around a black background.
# Each of these pixels represents the starting point for a spiraling pattern.
# To create the output grid, draw a clockwise spiral starting from each colored dot, using the dot's color.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    def get_next_position(x, y, direction):
        dx, dy = direction
        return x + dx, y + dy, (dx, dy)
    
    def get_next_direction(dx, dy):
        if dx == 1 and dy == 0:  # moving right
            return (0, 1)  # move down
        elif dx == 0 and dy == 1:  # moving down
            return (-1, 0)  # move left
        elif dx == -1 and dy == 0:  # moving left
            return (0, -1)  # move up
        elif dx == 0 and dy == -1:  # moving up
            return (1, 0)  # move right

    pixel_xs, pixel_ys = np.where(input_grid != Color.BLACK)
    for x, y in zip(pixel_xs, pixel_ys):
        color = input_grid[x, y]
        
        direction = (1, 0)
        step = 1
        steps_taken = 0
        changes = 0
        while True:
            for i in range(step):
                x, y, direction = get_next_position(x, y, direction)
                if 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]:
                    output_grid[x, y] = color
                else:
                    return output_grid
            
            direction = get_next_direction(*direction)
            steps_taken += 1
            if steps_taken % 2 == 0:
                step += 1
    
    return output_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(10, 15)
    input_grid = np.full((n, n), Color.BLACK)
    
    num_dots = np.random.randint(5, 8)
    for _ in range(num_dots):
        x, y = np.random.randint(0, n), np.random.randint(0, n)
        color = np.random.choice(Color.NOT_BLACK)
        input_grid[x, y] = color

    return input_grid