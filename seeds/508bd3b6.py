from common import *

import numpy as np
from typing import *

# concepts:
# bouncing

# description:
# In the input you will see a short diagonal teal line pointing at a red rectangle on a black background.
# To make the output, shoot outward from the teal line, but change the color to green. Reflect off the red rectangle.

def main(input_grid):
    # Plan:
    # 1. Detect the objects
    # 2. Determine the orientation of the teal line, and its endpoints
    # 3. Shoot a green line outward until it hits the red rectangle
    # 4. Reflect the green line off the red rectangle, continuing in green

    teal_line = detect_objects(input_grid, colors=[Color.TEAL], monochromatic=True, connectivity=8)
    assert len(teal_line) == 1, "There should be exactly one teal line"
    teal_line = list(teal_line)[0]
    red_rectangle = detect_objects(input_grid, colors=[Color.RED], monochromatic=True, connectivity=8)
    assert len(red_rectangle) == 1, "There should be exactly one red rectangle"
    red_rectangle = list(red_rectangle)[0]

    output_grid = input_grid.copy()

    # To get the orientation of a line, find the endpoints and compare their x and y coordinates
    x1, y1 = max( (x, y) for x, y in np.argwhere(teal_line == Color.TEAL) )
    x2, y2 = min( (x, y) for x, y in np.argwhere(teal_line == Color.TEAL) )
    direction12 = (int(np.sign(x2 - x1)), int(np.sign(y2 - y1)))
    direction21 = (-direction12[0], -direction12[1])

    # Try both (direction, x2, y2) and (-direction, x1, y1) as starting points
    for (dx,dy), start_x, start_y in [ (direction12, x2, y2), (direction21, x1, y1) ]:
        start_x += dx
        start_y += dy
        # Loop, shooting lines off of red things, until we run out of the canvas
        while 0 <= start_x < input_grid.shape[0] and 0 <= start_y < input_grid.shape[1]:
            stop_x, stop_y = draw_line(output_grid, start_x, start_y, direction=(dx,dy), color=Color.GREEN, stop_at_color=[Color.RED])

            # reflection geometry depends on if we hit the red rectangle on our left/right/up/down
            # did we hit the red rectangle on our right? 
            if stop_x+1 < output_grid.shape[0] and output_grid[stop_x+1, stop_y] != Color.BLACK:
                dx = -dx
            # did we hit the red rectangle on our left?
            elif stop_x-1 >= 0 and output_grid[stop_x-1, stop_y] != Color.BLACK:
                dx = -dx
            # did we hit the red rectangle on our bottom?
            elif stop_y+1 < output_grid.shape[1] and output_grid[stop_x, stop_y+1] != Color.BLACK:
                dy = -dy
            # did we hit the red rectangle on our top?
            elif stop_y-1 >= 0 and output_grid[stop_x, stop_y-1] != Color.BLACK:
                dy = -dy
            else:
                # didn't do any reflections, so stop
                break

            start_x, start_y = stop_x + dx, stop_y + dy
    
    return output_grid


def generate_input():
    # Make a grid with a red rectangle on the bottom and a teal diagonal line at the top pointing at it
    # Then randomly rotate to get a variety of orientations

    width, height = np.random.randint(10, 25), np.random.randint(8, 10)
    grid = np.full((width, height), Color.BLACK)

    red_height = np.random.randint(2, 5)
    grid[:, -red_height:] = Color.RED

    # Make a diagonal line, which always begins at the top
    line_x = np.random.randint(0, width//2)
    # always begins at the top
    line_y = 0

    draw_line(grid, line_x, line_y, direction=(1, 1), color=Color.TEAL, length=2)

    # randomly rotate to get a variety of orientations
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
