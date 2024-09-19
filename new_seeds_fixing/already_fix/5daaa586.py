from common import *
import numpy as np
from typing import *

# concepts:
# pattern extraction, pixel expanding

# description:
# In the input you will see four lines of different colors intersecting and forming a rectangle.
# Few pixels of one specific line's color are scattered in the grid.
# To make the output, you should cropped out the rectangle and extend the scatterd pixels to 
# the specific line which has same color as the scattered pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # Identify two vertical and two horizontal lines
    rows = np.where(np.all(output_grid != 0, axis=1))[0]
    columns = np.where(np.all(output_grid != 0, axis=0))[0]
    
    # Find out the color of the scattered pixels
    mask = np.ones(output_grid.shape, dtype=bool)
    mask[rows, :] = False
    mask[:, columns] = False
    color = output_grid[mask & (output_grid != Color.BLACK)][0]
    
    # Crop the grid by the rectangle formed by the four lines
    output_grid = output_grid[rows[0] : rows[1] + 1, columns[0] : columns[1] + 1]
    
    # Extend the scattered pixels to the line that has same color as the scattered pixels
    for x in range(len(output_grid)):
        for y in range(len(output_grid[0])):
            if output_grid[x, y] == color:
                if output_grid[0, y] == color:
                    draw_line(output_grid, x, y, end_x = 0, end_y = y, color = color)
                if output_grid[len(output_grid) - 1, y] == color:
                    draw_line(output_grid, x, y, end_x = len(output_grid) - 1, end_y = y, color = color)
                if output_grid[x, 0] == color:
                    draw_line(output_grid, x, y, end_x = x, end_y = 0, color = color)
                if output_grid[x, len(output_grid[0]) - 1] == color:
                    draw_line(output_grid, x, y, end_x = x, end_y = len(output_grid[0]) - 1, color = color)

    return output_grid

def generate_input() -> np.ndarray:
    # Create background grid with four lines in random position
    # Randomly generate the empty gaps between each two lines
    empty_rows = np.random.randint(1, 11, size=3)
    empty_columns = np.random.randint(1, 11, size=3)

    # Create the grid with the four lines with the empty gaps
    width, height = np.sum(empty_rows) + 2, np.sum(empty_columns) + 2
    grid = np.zeros((width, height), dtype=int)
    
    # Generate four different colors for four lines
    line_colors = np.random.choice(Color.NOT_BLACK, 4, replace=False)
    
    # Randomly determine order for placing colored lines
    lines_pos = [(empty_rows[0], 0), (np.sum(empty_rows[:2]) + 1, 0), (0, empty_columns[0]), (0, np.sum(empty_columns[:2]) + 1)]
    random.shuffle(lines_pos)
    for i in range(len(lines_pos)):
        line_x, line_y = lines_pos[i]
        if line_y == 0:
            draw_line(grid = grid, x = line_x, y = 0, end_x = line_x, end_y = height, color = line_colors[i])
        if line_x == 0:
            draw_line(grid = grid, x = 0, y = line_y, end_x = width, end_y = line_y, color = line_colors[i])
    
    # Randomly choose a color from line and create several scattered pixels of that color
    scattered_pixel_color = random.choice(line_colors)
    for x in range(width):
        for y in range(height):
            if grid[x, y] == Color.BLACK and random.randint(0, 15) == 0:
                grid[x, y] = scattered_pixel_color
    
    # Ensure the cells in the central square are partly filled with the chosen color
    for i in range(random.randint(3, 6)):
        x = random.randint(empty_rows[0] + 1, np.sum(empty_rows[:2]))
        y = random.randint(empty_columns[0] + 1, np.sum(empty_columns[:2]))
        grid[x, y] = scattered_pixel_color
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
