from common import *

import numpy as np
from typing import *

# concepts:
# pixel patterns, expansion, color sequence

# description:
# In the input you will see a grid with a cross pattern. Each pixel in the cross has a different color.
# To make the output, you should expand the cross right/left/top/bottom following the original color sequence of the cross.

def main(input_grid):
    # Plan:
    # 1. Parse the input and create output canvas to draw on top of
    # 2. Extract the vertical and horizontal parts of the cross, and make note of the coordinate of the middle
    # 3. Expand the horizontal part to the right and left, aligned with the middle y coordinate
    # 4. Expand the vertical part to the top and bottom, aligned with the middle x coordinate    

    # 1. Input parsing
    # Extract the cross, which has many colors and so is not monochromatic.
    objects = find_connected_components(input_grid, monochromatic=False)
    assert len(objects) == 1, "exactly one cross expected"
    obj = objects[0]
    cross_x, cross_y = object_position(obj)

    # Create output grid, which we are going to draw on top of, so we start with the input grid
    output_grid = input_grid.copy()
    width, height = input_grid.shape

    # 2. Cross analysis: Extract subsprites, get the middle
    # Extract the horizontal/vertical parts of the cross sprite by figuring out where its middle is (where the horizontal and vertical lines meet)
    sprite = crop(obj)
    cross_width, cross_height = sprite.shape
    # Middle is where they meet
    cross_middle_x = next( x for x in range(cross_width) if np.all(sprite[x, :] != Color.BLACK) )
    cross_middle_y = next( y for y in range(cross_height) if np.all(sprite[:, y] != Color.BLACK) )
    # Extract the horizontal and vertical parts of the cross
    vertical_sprite = sprite[cross_middle_x:cross_middle_x+1, :]
    horizontal_sprite = sprite[:, cross_middle_y:cross_middle_y+1]

    # 3. Expand the horizontal line to the right and left
    x_start, y_start, len_line = cross_x, cross_y + cross_middle_y, cross_width
    for i in range(x_start, width, len_line):
        blit_sprite(output_grid, horizontal_sprite, x=i, y=y_start)
    for i in range(x_start, -(len_line), -len_line):
        blit_sprite(output_grid, horizontal_sprite, x=i, y=y_start)
    
    # 4. Expand the vertical line to the top and bottom
    x_start, y_start, len_line = cross_x + cross_middle_x, cross_y, cross_height
    for i in range(y_start, height, len_line):
        blit_sprite(output_grid, vertical_sprite, x=x_start, y=i)
    for i in range(y_start, -(len_line), -len_line):
        blit_sprite(output_grid, vertical_sprite, x=x_start, y=i)
        
    return output_grid

def generate_input():
    # Generate the background grid
    width, height = np.random.randint(20, 30, size=2)
    grid = np.full((width, height), Color.BLACK)

    # Randomly choose the number of colors
    num_colors = np.random.randint(2, 5)
    colors = np.random.choice(Color.NOT_BLACK, size=num_colors, replace=False)

    # Generate a line with these colors in sequence
    line = np.full((num_colors, 1), Color.BLACK)
    for i in range(num_colors):
        line[i, 0] = colors[i]

    # form a cross pattern randomly
    cross_points = random.randint(0, num_colors - 1)
    sprite = np.full((num_colors, num_colors), Color.BLACK)
    line_t = np.transpose(line)
    blit_sprite(sprite, line, x=0, y=cross_points)
    blit_sprite(sprite, line_t, x=cross_points, y=0)

    # Randomly rotate the pattern
    sprite = np.rot90(sprite, k=np.random.randint(4))

    # Randomly place the pattern on the grid
    x, y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x=x, y=y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
