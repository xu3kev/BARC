from common import *

import numpy as np
from typing import *

# concepts:
# growing

# description:
# In the input you will see a grid with some green rectangles. Each rectangle has one red pixel on one of its borders.
# To make the output, you should extend the green line of each rectangle to the border of the grid 
# in the direction of the red pixel and between the red pixel, each line should have the same size as the width - 1 of the rectangle.
# Also you should draw a red line from the red pixel to the border of the grid.


def main(input_grid):
    # Initialize the output grid
    output_grid = np.copy(input_grid)
    
    rectangle_color = Color.GREEN
    indicator_color = Color.RED

    # Get all the green rectangles on the grid
    rectangles = find_connected_components(grid=input_grid, connectivity=4, monochromatic=False)
    for rectangle in rectangles:
        cropped_rectangle = crop(grid=rectangle)
        x, y, width, height = bounding_box(grid=rectangle)

        # Find the red indicator pixel on the border of the rectangle
        for i, j in np.ndindex(width, height):
            if cropped_rectangle[i, j] == Color.RED:
                break
        red_x, red_y = i, j
        rela_x, rela_y = x + red_x, y + red_y

        # If one the left border, extend the line to the left
        if red_x == 0:
            draw_line(grid=output_grid, x=rela_x, y=rela_y, direction=(-1, 0), color=indicator_color)
            # Extend green line to the left with same size of width - 1
            for i in range(1, width):
                draw_line(grid=output_grid, x=rela_x, y=rela_y - i, direction=(-1, 0), color=rectangle_color)
                draw_line(grid=output_grid, x=rela_x, y=rela_y + i, direction=(-1, 0), color=rectangle_color)

        # If one the right border, extend the line to the right
        if red_x == width - 1:
            draw_line(grid=output_grid, x=rela_x, y=rela_y, direction=(1, 0), color=indicator_color)
            # Extend green line to the right with same size of width - 1
            for i in range(1, width):
                draw_line(grid=output_grid, x=rela_x, y=rela_y - i, direction=(1, 0), color=rectangle_color)
                draw_line(grid=output_grid, x=rela_x, y=rela_y + i, direction=(1, 0), color=rectangle_color)
        
        # If one the top border, extend the line to the top
        if red_y == 0:
            draw_line(grid=output_grid, x=rela_x, y=rela_y, direction=(0, -1), color=indicator_color)
            # Extend green line to the top with same size of height - 1
            for i in range(1, height):
                draw_line(grid=output_grid, x=rela_x - i, y=rela_y, direction=(0, -1), color=rectangle_color)
                draw_line(grid=output_grid, x=rela_x + i, y=rela_y, direction=(0, -1), color=rectangle_color)
        
        # If one the bottom border, extend the line to the bottom
        if red_y == height - 1:
            draw_line(grid=output_grid, x=rela_x, y=rela_y, direction=(0, 1), color=indicator_color)
            # Extend green line to the bottom with same size of height - 1
            for i in range(1, height):
                draw_line(grid=output_grid, x=rela_x - i, y=rela_y, direction=(0, 1), color=rectangle_color)
                draw_line(grid=output_grid, x=rela_x + i, y=rela_y, direction=(0, 1), color=rectangle_color)

    return output_grid

def generate_input():
    # Create the background grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.zeros((n, m), dtype=int)

    rectangle_num = 2
    rectangle_color = Color.GREEN
    indicator_color = Color.RED

    # Draw rectangles on the grid
    for i in range(rectangle_num):
        width, height = np.random.randint(3, 20), np.random.randint(3, 20)

        # The width should be twice smaller than the height
        while (width * 2 + 2) >= height:
            width, height = np.random.randint(3, 20), np.random.randint(3, 20)

        green_rectangle = np.ones((width, height), dtype=int) * rectangle_color

        # Place one indicator pixel on one random border of the rectangle
        # Spare enough space for the extend line with the same size of width - 1
        x_coord = np.random.choice([0, width - 1])
        y_coord = np.random.choice(range(width + 1, height - (width + 1)))
        green_rectangle[x_coord, y_coord] = indicator_color
        if_rotate = np.random.choice([True, False])
        if if_rotate:
            green_rectangle = np.rot90(green_rectangle)
            x_coord, y_coord = y_coord, x_coord

        # Place the rectangle on the grid
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=green_rectangle, padding=2, padding_connectivity=8)
        
        # Check if there is no space for the rectangle
        except:
            return generate_input()
        grid = blit_sprite(grid=grid, sprite=green_rectangle, x=x, y=y)

    # Check if the generated grid is valid
    transformed_grid = main(grid)
    objects = find_connected_components(grid=transformed_grid, connectivity=4, monochromatic=False)

    # After transformation, the two objects should not touch each other
    if len(objects) != rectangle_num:
        # Regenerate the grid
        return generate_input()

    return grid
    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
