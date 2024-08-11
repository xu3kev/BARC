import numpy as np
from typing import *
from common import *

# concepts:
# symmetry, surrounding, growth, pathfinding

# description:
# The input will be a grid with multiple objects and a single "seed" pixel of a different color.
# The seed pixel will start a "growth" process.
# The growth will spread symmetrically in each direction.
# The direction of growth will be determined by neighboring same-color pixels.
# The same-color pixels (any color different from black) will act as barriers.
# The objective is to fill the entire grid where possible with the growth color, while ensuring symmetry in growth direction.

def main(input_grid):
    output_grid = np.copy(input_grid)
    growth_color = None
    seed_coords = None

    # Step 1: Find the seed pixel and identify the growth color
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != Color.BLACK:
                growth_color = input_grid[i, j]
                seed_coords = (i, j)
                break
        if growth_color:
            break

    if not growth_color:
        return output_grid  # No growth color found

    # Step 2: Perform growth from the seed point, stopping at any non-black pixel
    queue = [seed_coords]
    while queue:
        x, y = queue.pop(0)
        if output_grid[x, y] == Color.BLACK:
            output_grid[x, y] = growth_color
        
        # Check all 4-connected neighbors for open space or barriers
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]):
                if (output_grid[nx, ny] == Color.BLACK):
                    if ((0 <= 2 * nx - x < input_grid.shape[0] and 0 <= 2 * ny - y < input_grid.shape[1])):
                        # Check symmetry constraint
                        if (input_grid[2 * nx - x, 2 * ny - y] != Color.BLACK):
                            queue.append((nx, ny))
                        else:
                            output_grid[nx, ny] = growth_color

    return output_grid


# Input generation function
def generate_input():
    # create a grid filled with black pixels
    grid = np.zeros((9, 9), dtype=int)
    
    # randomly place objects with random colors
    for _ in range(np.random.randint(5, 10)):
        color = np.random.choice(Color.NOT_BLACK)
        width, height = np.random.randint(1, 4), np.random.randint(1, 4)
        sprite = random_sprite(width, height, color_palette=[color], connectivity=4)
        x, y = random_free_location_for_object(grid, sprite)
        blit(grid, sprite, x, y)
    
    # randomly place a seed pixel of new growth color
    growth_color = np.random.choice([col for col in Color.NOT_BLACK if col not in grid])
    seed_x, seed_y = np.random.randint(0, grid.shape[0]), np.random.randint(0, grid.shape[1])
    grid[seed_x, seed_y] = growth_color
    
    return grid