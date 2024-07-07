from common import *

import numpy as np
from typing import *

# concepts:
# connectivity

# description:
# In the input image you will see several teal pixels and two 2x2 red squares on the black background.
# If the 2x2 red squares are connected by a path of teal pixels, then output a 1x1 teal grid, otherwise, output a 1x1 black grid. 

def main(input_grid):
    # make output grid
    output_grid = np.zeros((1,1), dtype=int)

    # get just the red squares
    red_squares = np.zeros_like(input_grid)
    red_squares[input_grid == Color.RED] = Color.RED

    # get all components that are connected, regardless of color
    connected_components = find_connected_components(input_grid, connectivity=4, monochromatic=False)

    # check each connected component to see if it contains both red squares
    for connected_component in connected_components:
        # if it contains both red squares, output teal grid
        if np.all(connected_component[red_squares == Color.RED] == Color.RED):         
            output_grid[:,:] = Color.TEAL
            return output_grid

    # if none of the connected components contain both red squares, output black grid
    output_grid[:,:] = Color.BLACK
    return output_grid


def generate_input():
    # make a black grid first as background
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # make a 2x2 red square sprite
    red_square_sprite = np.full((2,2), Color.RED, dtype=int)

    # place a red square sprite at two random places on the grid
    x1, y1 = random_free_location_for_sprite(grid, red_square_sprite, padding=1)
    blit_sprite(grid, red_square_sprite, x1, y1)
    x2, y2 = random_free_location_for_sprite(grid, red_square_sprite, padding=1)
    blit_sprite(grid, red_square_sprite, x2, y2)

    # check that the red squares do not touch
    # if they do, then try again
    if contact(object1=red_square_sprite, object2=red_square_sprite, x1=x1, y1=y1, x2=x2, y2=y2):
        return generate_input()

    # sprinkle teal pixels over the black parts of the grid so they cover roughly a third of it
    for _ in range(n * m // 3):
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
        # do not sprinkle teal pixels on top of red ones
        if grid[x, y] != Color.RED:
            grid[x, y] = Color.TEAL
    
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)