from common import *

import numpy as np
from typing import *

black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

# concepts:
# collision detection, sliding objects

# description:
# In the input you will see a teal 2x2 square and a red object (the red object might be irregular in its shape)
# Slide the red object in any of the four directions until it just touches the teal square

def main(input_grid):

    # get just the teal object
    teal_object = np.zeros_like(input_grid)
    teal_object[input_grid == teal] = teal

    # get just the red object
    red_object = np.zeros_like(input_grid)
    red_object[input_grid == red] = red
    
    # the 4 sliding direction of left, up, down, right
    directions = [np.array([0, -1]), np.array([-1, 0]), np.array([1, 0]), np.array([0, 1])]

    # all directions by magnitudes 1, 2, 3, ... maximum amount
    for i in range(1, max(input_grid.shape)):
        for direction in directions:
            dx, dy = direction * i
            if collision(object1=teal_object, object2=red_object, x2=dx, y2=dy):
                # we have to subtract 1 from the magnitude because the last move made them collide, rather than just touch
                i -= 1
                dx, dy = direction * i

                output_grid = np.copy(teal_object)
                blit(output_grid, red_object, dx, dy, transparent=black)

                return output_grid
            
    assert 0, "No valid slide found"

def generate_input():
    # make a black grid first as background, roughly 5 x 5 to 10x10 works
    n, m = random.randint(5, 20), random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)

    # make a 2x2 teal square, put it somewhere random on the grid
    x, y = random.randint(0, n - 2), random.randint(0, m - 2)
    grid[x:x+2, y:y+2] = teal

    # make a random sprite of [3,4] x [3,4] with a random symmetry type and the color red
    sprite = random_sprite([3,4], [3,4], symmetry="not_symmetric", color_palette=[red])

    # put the sprite somewhere random on the grid
    x, y = random_free_location_for_object(grid, sprite, background=black)

    blit(grid, sprite, x, y, transparent=black)    

    # check that we could slide the object either vertically or horizontally in order to touch the red square
    # this will be true if there is a row or column that has both red and blue
    for i in range(n):
        if teal in grid[i, :] and red in grid[i, :]:
            return grid
    for j in range(m):
        if teal in grid[:, j] and red in grid[:, j]:
            return grid
    
    # if not, try again
    return generate_input()


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)