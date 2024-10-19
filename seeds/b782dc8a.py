from common import *

import numpy as np
from typing import *

# concepts:
# maze, path finding

# description:
# In the input you will see a maze with a path that has two indicator pixels of different colors.
# To make the output, fill all reachable parts of the maze starting with the indicator pixels and alternating colors.

def main(input_grid):
    # Output grid draws on top of the input grid
    output_grid = input_grid.copy()

    # Parse the input
    maze_color = Color.TEAL
    indicator_colors = [ color for color in object_colors(input_grid, background=Color.BLACK) if color != maze_color]
    assert len(indicator_colors) == 2, "expected exactly two indicator colors"
    
    # Fill the path with alternating colors in turn
    def fill_maze(cur_color, next_color, x, y, grid):
        width, height = grid.shape
        # Search outward in four directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x < width and 0 <= new_y < height and grid[new_x, new_y] == Color.BLACK:
                grid[new_x, new_y] = next_color
                # Change the next color to the current color: swap current and next
                fill_maze(next_color, cur_color, new_x, new_y, grid)
    
    # Fill the path with two colors
    # Start to fill the path with the pixel that already has the path_color
    for x, y in np.argwhere((input_grid != Color.BLACK) & (input_grid != maze_color)):
        cur_color = input_grid[x, y]
        next_color = indicator_colors[0] if cur_color == indicator_colors[1] else indicator_colors[1]
        fill_maze(cur_color, next_color, x, y, output_grid)

    return output_grid

def generate_input():
    # Create the background grid
    width, height = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.full((width, height), Color.BLACK)

    # function to check if the surrounding pixels are all black
    def check_available(x, y, grid, directions):
        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x and new_x < grid.shape[0] and 0 <= new_y and new_y < grid.shape[1] and grid[new_x, new_y] != Color.BLACK:
                return False
        return True
    
    # function for random walk to generate the maze
    def random_walk(color, grid, x, y):
        # Four walking directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Randomly choose one available direction
        random.shuffle(directions)
        for direction in directions:
            cur_x, cur_y = x + direction[0], y + direction[1]
            # Check if the next position is out of the grid
            if cur_x < 0 or cur_x >= width or cur_y < 0 or cur_y >= height:
                continue

            # Check if the next position touch other maze path
            rest_directions = [d for d in directions if d != (-direction[0], -direction[1])]
            if check_available(cur_x, cur_y, grid, rest_directions):
                # If not, mark the next position as the maze path
                # And continue the random walking
                grid[cur_x, cur_y] = color
                random_walk(color, grid, cur_x, cur_y)
                break

    # The color for the maze path        
    maze_color = Color.TEAL

    # Iterate over the grid to generate the maze
    for x, y in np.argwhere(grid == Color.BLACK):
        # If the current position is not empty, skip
        if grid[x, y] != Color.BLACK:
            continue

        # Check if the surrounding pixels are all black, which means we can start the random walking
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        if check_available(x, y, grid, directions):
            # Start the random walking
            grid[x, y] = maze_color

            # Avoid the exception `maximum recursion depth exceeded`
            try:
                random_walk(maze_color, grid, x, y)
            except:
                continue
    
    # The path has two colors which appear in turn
    path_color = np.random.choice([color for color in Color.NOT_BLACK if color != maze_color], 2, replace=False)

    # Mark the longest path to be colored to the path_color in turn
    objects = find_connected_components(grid, background=maze_color, connectivity=4, monochromatic=True)
    path = max(objects, key=lambda x: np.sum(x == Color.BLACK))

    # Find one empty position to start the path
    x, y = random.choice(np.argwhere(path == Color.BLACK))

    # Color the position with one of the path_color
    grid[x, y] = path_color[0]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        if 0 <= x + direction[0] < width and 0 <= y + direction[1] < height and grid[x + direction[0], y + direction[1]] == Color.BLACK:
            # Color the surrounding pixels with the other path_color
            # Which indicates the color should be changed in the next step
            grid[x + direction[0], y + direction[1]] = path_color[1]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
