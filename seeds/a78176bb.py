from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines

# description:
# In the input you will see a grid with a diagonal line and gray objects touching it. The grey objects are all right triangles.
# To make the output grid, draw additional diagonal lines in the same color emanating from the tip of the grey objects. Delete the grey objects.

def main(input_grid):
    # Plan:
    # 1. Find the diagonal (it's the only one) and greys
    # 2. For each grey, find the tip
    # 3. ... and draw a diagonal line in the same color and same direction
    # 4. Delete the greys
    
    # 1. Input parsing: Find the grey objects, and then extract by color everything that is not grey
    background = Color.BLACK
    grey_objects = [ obj for obj in find_connected_components(input_grid, connectivity=4, monochromatic=True, background=background)
                     if Color.GREY in object_colors(obj, background=background) ]
    # extracting the diagonal by color: we know it's just everything that's not grey
    diagonal_object = input_grid.copy()
    diagonal_object[diagonal_object == Color.GREY] = background

    # Parse out the color and directionbof the diagonal
    diagonal_color = object_colors(diagonal_object, background=background)[0]
    if crop(diagonal_object, background=background)[0,0] == diagonal_color:
        diagonal_direction = (1,1) # down-right
    else:
        diagonal_direction = (-1,1) # up-right

    # We draw on top of the input, so copy it
    output_grid = input_grid.copy()

    # 2. Find the tips of the grey objects
    for grey_object in grey_objects:
        # The tip is the bordering pixel farthest away from the diagonal
        bordering_pixels_mask = object_neighbors(grey_object, connectivity=8, background=background)
        def distance_to_object(x, y, obj):
            return min( np.linalg.norm([x - x2, y - y2]) for x2, y2 in np.argwhere(obj != background) )
        tip = max( np.argwhere(bordering_pixels_mask), key=lambda xy: distance_to_object(xy[0], xy[1], diagonal_object) )
        tip_x, tip_y = tip

        # 3. Draw the diagonal line
        draw_line(output_grid, tip_x, tip_y, direction=diagonal_direction, color=diagonal_color)
        draw_line(output_grid, tip_x, tip_y, direction=(-diagonal_direction[0], -diagonal_direction[1]), color=diagonal_color)

    # 4. Delete grey
    output_grid[output_grid == Color.GREY] = background

    return output_grid

def generate_input():
    # Generate the background grid
    grid_len = np.random.randint(10, 20)
    grid = np.full((grid_len, grid_len), Color.BLACK)

    diagonal_color = random.choice([ color for color in Color.NOT_BLACK if color != Color.GREY ])
    diagonal_direction = (1,1) # rotate at the end in order to get variety of orientations5
    diagonal_x, diagonal_y = random.choice(np.argwhere(grid == Color.BLACK))
    draw_line(grid, diagonal_x, diagonal_y, direction=diagonal_direction, color=diagonal_color)
    draw_line(grid, diagonal_x, diagonal_y, direction=(-diagonal_direction[0], -diagonal_direction[1]), color=diagonal_color)

    # Randomly generate grey objects and place them on the grid so they are touching the diagonal
    num_grey_objects = random.choice([1, 2, 3])
    for _ in range(num_grey_objects):
        # the grey sprite is a right-triangle of random size
        grey_size = np.random.randint(2, 5)
        grey_sprite = np.full((grey_size, grey_size), Color.BLACK)
        for x in range(grey_size):
            for y in range(grey_size):
                if x<=y: grey_sprite[x, y] = Color.GREY
        
        # random orientation
        if np.random.rand() < 0.5: grey_sprite = grey_sprite.T

        # find a placement so it touches
        while True:
            x, y = random_free_location_for_sprite(grid, sprite=grey_sprite)
            diagonal_mask = (grid == diagonal_color)
            if contact(object1=diagonal_mask, object2=grey_sprite, x2=x, y2=y, background=Color.BLACK):
                break
        blit_sprite(grid, grey_sprite, x, y)
    
    # Randomly rotate the grid
    grid = np.rot90(grid, k=np.random.randint(4))

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
