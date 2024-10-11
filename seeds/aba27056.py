from common import *

import numpy as np
from typing import *

# concepts:
# cups, filling

# description:
# In the input you will see a cups, meaning an almost-enclosed shape with a small opening on one of its sides, and empty space (black pixels) inside.
# To make the output grid, you should fill the interior of each cup with yellow, then shoot yellow out of the opening of the cup both straight out and diagonally from the edges of the opening.
# 

def main(input_grid):
    # Plan:
    # 1. Detect the cup
    # 2. Find the mask of the inside of the cup
    # 3. Find the mask of the opening of the cup (on one of its sides)
    # 4. Fill the cup with yellow
    # 5. Shoot pixels outward from the opening (straight out)
    # 6. Shoot pixels outward from the opening (diagonally out, from the edges)
    
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

    # 4. Fill the cup with yellow
    output_grid[inside_cup_mask] = Color.YELLOW

    # 5. Shoot pixels outward from the opening (straight out)
    # Find the direction of the opening, which is the unit vector that points from the center of the cup to the hole
    hole_x, hole_y = object_position(hole_mask, background=Color.BLACK, anchor='center')
    cup_x, cup_y = object_position(obj, background=Color.BLACK, anchor='center')
    direction = (int(np.sign(hole_x - cup_x)), int(np.sign(hole_y - cup_y)))
    # Loop over every boundary pixel and shoot outward
    for x, y in np.argwhere(hole_mask):
        draw_line(output_grid, x, y, direction=direction, color=Color.YELLOW)

    # 6. Shoot pixels outward from the opening (diagonally out, from the edges)
    # Find the two extremal points on the boundary of the hole, which are the points farthest away from each other
    points_on_boundary = np.argwhere(hole_mask)
    pt1, pt2 = max({ ( (x1,y1), (x2,y2) ) for x1,y1 in points_on_boundary for x2,y2 in points_on_boundary },
                   key=lambda pair: np.linalg.norm(np.array(pair[0]) - np.array(pair[1])))
    
    # For each of those points, shoot diagonal lines in all directions, but stop as soon as you hit something that's not black
    for pt in [pt1, pt2]:
        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw_line(output_grid, pt[0]+direction[0], pt[1]+direction[1], direction=direction, color=Color.YELLOW, stop_at_color=Color.NOT_BLACK)
    
    return output_grid

def generate_input():
    # Generate the grid with random size
    width = np.random.randint(8, 30)
    height = np.random.randint(8, 30)
    grid = np.full((width, height), Color.BLACK)

    # Pick a random width/height for this cup
    cup_width = np.random.randint(4, 8)
    cup_height = np.random.randint(3, 8)

    # Make a sprite, which is just going to be a blue outline of a rectangle with a hole at the top
    sprite = np.full((cup_width, cup_height), Color.BLACK)
    color = np.random.choice([ color for color in Color.NOT_BLACK if color != Color.YELLOW ])
    sprite[0, :] = color
    sprite[-1, :] = color
    sprite[:, 0] = color
    sprite[:, -1] = color

    # Make the hole centered at the top (variable size)
    hole_left_x = np.random.randint(1, cup_width//2+1)
    hole_right_x = cup_width - hole_left_x - 1
    hole_y = 0
    sprite[hole_left_x:hole_right_x+1, hole_y] = Color.BLACK

    # Find a random free location for it
    free_x, free_y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, sprite, free_x, free_y, background=Color.BLACK)

    # Do a random rotation, so the cup can face any direction
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
