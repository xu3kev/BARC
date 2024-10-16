from common import *

import numpy as np
from typing import *

# concepts:
# maze, path finding

# description:
# In the input you will see a maze with a path that has two indicator pixels of different colors.
# To make the output, fill the path with two colors in turn.

def main(input_grid):
    # Output grid transform from the input grid
    output_grid = input_grid.copy()

    # Find all the paths in the maze
    maze_color = Color.TEAL
    objects = find_connected_components(input_grid, background=Color.TEAL, connectivity=4, monochromatic=False)

    # Find the path with two indicator colors
    for object in objects:
        colors = np.unique(object)
        colors = [color for color in colors if color != Color.BLACK and color != maze_color]
        if len(colors) == 2:
            path_color = colors
            path_object = object
            break
    
    # Fill the path with two colors in turn
    def fill_the_grid(cur_color, next_color, x, y, grid):
        n, m = grid.shape
        # Search the path in four directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x < n and 0 <= new_y < m and grid[new_x, new_y] == Color.BLACK:
                grid[new_x, new_y] = next_color
                # Change the next color to the current color
                fill_the_grid(next_color, cur_color, new_x, new_y, grid)
    
    # Fill the path with two colors
    position_list = np.argwhere(path_object == path_color[0]).tolist() + np.argwhere(path_object == path_color[1]).tolist()
    
    # Start to fill the path with the pixel that already has the path_color
    for x, y in position_list:
        cur_color = path_object[x, y]
        next_color = path_color[0] if cur_color == path_color[1] else path_color[1]
        fill_the_grid(cur_color, next_color, x, y, output_grid)

    return output_grid

def generate_input():
    # Create the background grid
    n, m = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.full((n, m), Color.BLACK)

    # The function to check if the surrounding pixels are all black
    def check_available(x, y, grid, directions):
        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x and new_x < grid.shape[0] and 0 <= new_y and new_y < grid.shape[1] and grid[new_x, new_y] != Color.BLACK:
                return False
        return True
    
    # The function for random walking to generate the maze
    def random_walking(color, grid, x, y):
        # Four walking directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Randomly choose one available direction
        random.shuffle(directions)
        for direction in directions:
            cur_x, cur_y = x + direction[0], y + direction[1]
            # Check if the next position is out of the grid
            if cur_x < 0 or cur_x >= n or cur_y < 0 or cur_y >= m:
                continue

            # Check if the next position touch other maze path
            rest_directions = [d for d in directions if d != (-direction[0], -direction[1])]
            if check_available(cur_x, cur_y, grid, rest_directions):
                # If not, mark the next position as the maze path
                # And continue the random walking
                grid[cur_x, cur_y] = color
                random_walking(color, grid, cur_x, cur_y)
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
                random_walking(maze_color, grid, x, y)
            except:
                continue
    
    # The path has two colors which appear in turn
    path_color = np.random.choice([color for color in Color.NOT_BLACK if color != maze_color], 2, replace=False)

    # Mark the longest path to be colored to the path_color in turn
    objects = find_connected_components(grid, background=maze_color, connectivity=4, monochromatic=True)
    objects = sorted(objects, key=lambda x: np.sum(x == Color.BLACK), reverse=True)
    path = objects[0]

    # Find one empty position to start the path
    x, y = random_free_location_for_sprite(grid=path, sprite=np.array([[1]]))

    # Color the position with one of the path_color
    grid[x, y] = path_color[0]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        if 0 <= x + direction[0] < n and 0 <= y + direction[1] < m and grid[x + direction[0], y + direction[1]] == Color.BLACK:
            # Color the surrounding pixels with the other path_color
            # Which indicates the color should be changed in the next step
            grid[x + direction[0], y + direction[1]] = path_color[1]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
