from common import *

import numpy as np
from typing import *

# concepts:
# growing

# description:
# In the input you will see a grid with some green rectangles. Each rectangle has one red pixel on one of its borders.
# To make the output, you should extend the green region of each rectangle to the border of the grid in the direction of the red pixel, with the extent of the line increasing with the extent of the rectangle.
# Also you should draw a red line from the red pixel to the border of the grid.


def main(input_grid):
    # Initialize the output grid
    output_grid = np.copy(input_grid)
    
    rectangle_color = Color.GREEN
    indicator_color = Color.RED
    background = Color.BLACK

    # get all the green rectangles on the grid. because of the red pixel on the border of the rectangle, they are not monochromatic.
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=False, background=background)
    for obj in objects:
        # find the red indicator
        for red_x, red_y in np.argwhere(obj == indicator_color):
            break

        # Get the dimensions of the object, and its position
        x, y, width, height = bounding_box(obj, background=background)  

        # depending on which side of the rectangle that the indicator is on, we draw in different directions
        # left edge: draw to the left
        if red_x == x:
            # Extend the green rectangle to the left until it reaches the border
            output_grid[0:red_x, red_y-(width-1) : red_y+(width-1)+1] = rectangle_color
            # Draw the red line from the red pixel to the border
            draw_line(output_grid, x=red_x, y=red_y, direction=(-1, 0), color=indicator_color)
        elif red_x == x + width - 1:
            # Extend the green rectangle to the right until it reaches the border
            output_grid[red_x:, red_y-(width-1) : red_y+(width-1)+1] = rectangle_color
            # Draw the red line from the red pixel to the border
            draw_line(output_grid, x=red_x, y=red_y, direction=(1, 0), color=indicator_color)
        elif red_y == y:
            # Extend the green rectangle to the top until it reaches the border
            output_grid[red_x-(height-1) : red_x+(height-1)+1, 0:red_y] = rectangle_color
            # Draw the red line from the red pixel to the border
            draw_line(output_grid, x=red_x, y=red_y, direction=(0, -1), color=indicator_color)
        elif red_y == y + height - 1:
            # Extend the green rectangle to the bottom until it reaches the border
            output_grid[red_x-(height-1) : red_x+(height-1)+1, red_y:] = rectangle_color
            # Draw the red line from the red pixel to the border
            draw_line(output_grid, x=red_x, y=red_y, direction=(0, 1), color=indicator_color)
        else:
            assert False, "The red pixel is not on the border of the rectangle"

    return output_grid

def generate_input():
    # Create the background grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK)

    rectangle_num = 2
    rectangle_color = Color.GREEN
    indicator_color = Color.RED

    # Draw rectangles on the grid
    for i in range(rectangle_num):
        width, height = np.random.randint(3, 20), np.random.randint(3, 20)

        # The width should be twice smaller than the height
        while (width * 2 + 2) >= height:
            width, height = np.random.randint(3, 20), np.random.randint(3, 20)

        green_rectangle = np.full((width, height), rectangle_color)

        # Place one indicator pixel on one random border of the rectangle
        # Spare enough space for the extend line with the same size of width - 1
        x_coord = np.random.choice([0, width - 1])
        y_coord = np.random.choice(range(width + 1, height - (width + 1)))
        green_rectangle[x_coord, y_coord] = indicator_color
        # Randomly rotate the object so that we get a variety of orientations
        if np.random.choice([True, False]):
            green_rectangle = np.rot90(green_rectangle)
            x_coord, y_coord = y_coord, x_coord

        # Place the rectangle on the grid
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=green_rectangle, padding=2, padding_connectivity=8)        
        # Check if there is no space for the rectangle
        except:
            return generate_input()
        blit_sprite(grid, green_rectangle, x=x, y=y)

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
