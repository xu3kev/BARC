from common import *

import numpy as np
from typing import *

# concepts:
# collision detection, sliding objects

# description:
# In the input you will see a teal 2x2 square and a red object (the red object might be irregular in its shape)
# Slide the red object in any of the four directions until it just touches the teal square

def main(input_grid):

    # get just the teal object
    teal_object = np.zeros_like(input_grid)
    teal_object[input_grid == Color.TEAL] = Color.TEAL

    # get just the red object
    red_object = np.zeros_like(input_grid)
    red_object[input_grid == Color.RED] = Color.RED

    # the output grid starts with just the teal object, because we still need to figure out where the red object will be by sliding it
    output_grid = np.copy(teal_object)
    
    # consider sliding in the 4 cardinal directions, and consider sliding as far as possible
    possible_displacements = [ (slide_distance*dx, slide_distance*dy)
                               for slide_distance in range(max(input_grid.shape))
                               for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)] ]
    for x, y in possible_displacements:
        # check if the objects are touching after sliding
        translated_red_object = translate(red_object, x, y, background=Color.BLACK)
        if contact(object1=teal_object, object2=translated_red_object):
            # put the red object where it belongs
            blit_object(output_grid, translated_red_object, background=Color.BLACK)
            return output_grid
            
    assert 0, "No valid slide found"

def generate_input():
    # make a black grid first as background, roughly 5 x 5 to 10x10 works
    n, m = random.randint(5, 20), random.randint(5, 20)
    grid = np.full((n, m), Color.BLACK)

    # make a 2x2 teal square, put it somewhere random on the grid
    square_sprite = np.full((2, 2), Color.TEAL)
    x, y = random_free_location_for_sprite(grid, square_sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, square_sprite, x, y, background=Color.BLACK)

    # make a random sprite of [3,4] x [3,4] with a random symmetry type and the color red
    sprite = random_sprite([3,4], [3,4], symmetry="not_symmetric", color_palette=[Color.RED])

    # put the sprite somewhere random on the grid
    x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, sprite, x, y, background=Color.BLACK)    

    # check that we could slide the object either vertically or horizontally in order to touch the red square
    # this will be true if there is a row or column that has both red and blue
    for x in range(n):
        if Color.TEAL in grid[x, :] and Color.RED in grid[x, :]:
            return grid
    for y in range(m):
        if Color.TEAL in grid[:, y] and Color.RED in grid[:, y]:
            return grid
    
    # if not, try again
    return generate_input()


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)