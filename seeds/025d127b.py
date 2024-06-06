from common import *

import numpy as np
from typing import *

black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

# concepts:
# objects

# description:
# In the input you will see a set of objects, each consisting of a horizontal top/bottom and diagonal left/right edges
# To make the output shift the whole object right *except* for the bottom edge and the bottommost pixel of the right diagonal edge (which stay put)

def main(input_grid: np.ndarray) -> np.ndarray:
    # find the connected components, which are monochromatic objects
    objects = find_connected_components(input_grid, background=black, connectivity=8, monochromatic=True)

    output_grid = np.zeros_like(input_grid)

    for obj in objects:
        # separate the object into the part that moves right, and the part that stays put
        # the part that moves right is everything except the bottom edge and the bottommost pixel of the right diagonal edge
        object_mask = obj != black
        staying_part = np.copy(object_mask)
        color = np.unique(obj)[1]

        # find the bottom right-hand corner
        # this is the pixel that has the biggest x and the biggest y
        biggest_x = np.argwhere(object_mask)[:,0].max()
        biggest_y = np.argwhere(object_mask)[:,1].max()

        # everything above the bottom bar doesn't stay put (except for the bottom pixel of the right diagonal edge)
        staying_part[:, :biggest_y] = False
        staying_part[biggest_x, biggest_y-1] = True 

        # the part that moves right is the opposite of the part that stays put
        moving_part = object_mask & ~staying_part

        # move it right by one pixel
        moved_part = np.roll(moving_part, 1, axis=0)

        # combine the moving and staying parts
        output_grid[moved_part] = color
        output_grid[staying_part] = color

    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 30), np.random.randint(10, 30)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(1, 3)

    for _ in range(n_objects):
        color = np.random.randint(1, 10)

        bar_width = np.random.randint(3, n//2)
        side_height = np.random.randint(3, m - bar_width)

        width, height = bar_width+side_height, side_height
        obj = np.zeros((width, height), dtype=int)

        # make the horizontal top edge
        obj[:bar_width+1, 0] = color
        # make the horizontal bottom edge
        obj[-bar_width:, -1] = color
        # make the diagonal left edge
        for i in range(side_height):
            obj[i, i] = color
        # make the diagonal right edge
        for i in range(side_height-1):
            obj[bar_width+i+1, i] = color

        # place the object randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_object(grid, obj, background=black)
        except:
            continue

        blit(grid, obj, x, y, transparent=black)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)