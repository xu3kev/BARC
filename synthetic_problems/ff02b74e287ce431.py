from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, borders, repeating pattern

# description:
# In the input, you will see a black grid with two sets of colored pixels.
# One set (A) will be scattered along one edge, while the other set (B) will be in the middle forming a line. The line pixels' color is treated as obstacles.
# To create the output, extend lines from the edge pixels towards the opposite edge.
# Lines should bend but cannot overlap with the obstacle pixels in a vertical or horizontal path.

def main(input_grid):
    def is_in_bounds(x, y, height, width):
        return 0 <= x < height and 0 <= y < width
    
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the edge color pixels and the middle line color pixels
    edge_color, middle_line_color = None, None
    edge_pixels = []
    middle_line_pixels = []

    # Detect edge and middle colors
    for x in range(height):
        for y in range(width):
            if x == 0 or y == 0 or x == height - 1 or y == width - 1:
                if input_grid[x, y] != Color.BLACK:
                    if edge_color is None:
                        edge_color = input_grid[x, y]
                    if input_grid[x, y] == edge_color:
                        edge_pixels.append((x, y))
            elif input_grid[x, y] != Color.BLACK:
                if middle_line_color is None:
                    middle_line_color = input_grid[x, y]
                if input_grid[x, y] == middle_line_color:
                    middle_line_pixels.append((x, y))

    # Define directions for expansion
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    # Draw lines from edge pixels towards the opposite edge
    for (start_x, start_y) in edge_pixels:
        queue = [(start_x, start_y)]
        visited = set(queue)
        while queue:
            x, y = queue.pop(0)
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_in_bounds(new_x, new_y, height, width) and (new_x, new_y) not in visited:
                    if input_grid[new_x, new_y] == Color.BLACK:
                        output_grid[new_x, new_y] = edge_color
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))
                    elif input_grid[new_x, new_y] == middle_line_color:
                        # Bypass middle pixels
                        if dx == 1 or dx == -1:
                            if is_in_bounds(new_x + dy, new_y, height, width) and (new_x + dy, new_y) not in visited and input_grid[new_x + dy, new_y] == Color.BLACK:
                                output_grid[new_x + dy, new_y] = edge_color
                                queue.append((new_x + dy, new_y))
                                visited.add((new_x + dy, new_y))
                        if dy == 1 or dy == -1:
                            if is_in_bounds(new_x, new_y + dx, height, width) and (new_x, new_y + dx) not in visited and input_grid[new_x, new_y + dx] == Color.BLACK:
                                output_grid[new_x, new_y + dx] = edge_color
                                queue.append((new_x, new_y + dx))
                                visited.add((new_x, new_y + dx))

    return output_grid


def generate_input():
    # generate a grid with two sets of colored pixels, one along an edge and another forming a horizontal or vertical line in the middle
    height = np.random.randint(10, 20)
    width = np.random.randint(10, 20)
    grid = np.full((height, width), Color.BLACK)

    # Choose colors
    edge_color = np.random.choice(Color.NOT_BLACK)
    middle_line_color = np.random.choice([c for c in Color.NOT_BLACK if c != edge_color])

    # Scatter edge color pixels along one edge
    edge_length = np.random.randint(3, min(height, width) - 2)
    if np.random.rand() < 0.5:
        # Horizontal edge
        i = np.random.randint(0, 2) * (height - 1)
        for _ in range(edge_length):
            grid[i, np.random.randint(1, width - 1)] = edge_color
    else:
        # Vertical edge
        j = np.random.randint(0, 2) * (width - 1)
        for _ in range(edge_length):
            grid[np.random.randint(1, height - 1), j] = edge_color

    # Form a horizontal or vertical middle line with middle line color
    if np.random.rand() < 0.5:
        i = height // 2
        for j in range(1, width - 1):
            grid[i, j] = middle_line_color
    else:
        j = width // 2
        for i in range(1, height - 1):
            grid[i, j] = middle_line_color

    return grid