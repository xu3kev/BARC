from common import *

import numpy as np
from typing import *

# concepts:
# cups, filling

# description:
# In the input you will see grey cups, meaning an almost-enclosed shape with a small opening on one of its sides, and empty space (black pixels) inside.
# To make the output grid, you should fill the interior of each cup with teal, then shoot teal out of the opening of the cup straight out in a line.

def main(input_grid):
    # Plan:
    # 1. Detect the cup
    # 2. Find the mask of the inside of the cup
    # 3. Find the mask of the opening of the cup (on one of its sides)
    # 4. Fill the cup with teal
    # 5. Shoot pixels outward from the opening (straight out)
    
    # 1. Detect cup
    objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK)
    assert len(objects) == 1, "There should be exactly one cup"
    obj = list(objects)[0]

    output_grid = input_grid.copy()

    # 2. Extract what's inside the cup (as its own object), which is everything in the bounding box that is not the object itself
    cup_x, cup_y, cup_width, cup_height = bounding_box(obj)
    inside_cup_mask = np.zeros_like(input_grid, dtype=bool)
    inside_cup_mask[cup_x:cup_x+cup_width, cup_y:cup_y+cup_height] = True
    inside_cup_mask = inside_cup_mask & (obj == Color.BLACK)

    # 3. Extract the hole in the cup, which is what's inside and on the boundary of the bounding box
    # what's inside...
    hole_mask = inside_cup_mask.copy()
    # ...and then we need to remove anything not on the boundary
    hole_mask[cup_x+1 : cup_x+cup_width-1, cup_y+1 : cup_y+cup_height-1] = False

    # 4. Fill the cup with teal
    output_grid[inside_cup_mask] = Color.TEAL

    # 5. Shoot pixels outward from the opening (straight out)
    # Find the direction of the opening, which is the unit vector that points away from the interior
    for cardinal_direction in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
        dx, dy = cardinal_direction
        hole_x, hole_y = object_position(hole_mask, background=Color.BLACK, anchor='center')
        if inside_cup_mask[hole_x - dx, hole_y - dy]:
            direction = cardinal_direction
            break
    # Loop over every boundary pixel and shoot outward
    for x, y in np.argwhere(hole_mask):
        draw_line(output_grid, x, y, direction=direction, color=Color.TEAL)
    return output_grid

def generate_input():
    # Generate the grid with random size
    width = np.random.randint(8, 30)
    height = np.random.randint(8, 30)
    grid = np.full((width, height), Color.BLACK)

    # Pick a random width/height for this cup
    cup_width = np.random.randint(4, 8)
    cup_height = np.random.randint(3, 8)

    # Make a sprite, which is just going to be a grey outline of a rectangle with a hole on one of its sides
    sprite = np.full((cup_width, cup_height), Color.BLACK)
    color = random.choice([ color for color in Color.NOT_BLACK if color != Color.TEAL ])
    sprite[0, :] = color
    sprite[-1, :] = color
    sprite[:, 0] = color
    sprite[:, -1] = color

    # Make the hole randomly somewhere on the edges (but not in the corners)
    edges_but_not_corners = [ (0, y) for y in range(1, cup_height-1) ] + [ (cup_width-1, y) for y in range(1, cup_height-1) ] + [ (x, 0) for x in range(1, cup_width-1) ] + [ (x, cup_height-1) for x in range(1, cup_width-1) ]
    hole_x, hole_y = random.choice(edges_but_not_corners)
    sprite[hole_x, hole_y] = Color.BLACK

    # Find a random free location for it
    free_x, free_y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, sprite, free_x, free_y, background=Color.BLACK)

    return grid    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
