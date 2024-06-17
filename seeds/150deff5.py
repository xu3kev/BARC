from common import *

import numpy as np
from typing import *

# concepts:
# search, color change

# description:
# In the input you will see grey-colored regions on a medium sized black canvas. These regions are comprised of 2x2 squares and 1x3/3x1 rectangles, but this might be hard to see because regions might be touching.
# To make the output, *search* for a way to break the input up into 2x2 squares and 1x3/3x1 rectangles, and color them as follows:
# 1. Color teal the 2x2 squares
# 2. Color red the 1x3/3x1 rectangles

def search_for_decompositions(grid: np.ndarray):

    # recursively enumerate all possible decompositions of the grid
    # loop over all possible object locations and check if there might be something there
    # if there is, try removing it and recursively searching for the rest of the objects
    # yields a stream of possible decompositions, each of which is a list of object masks 

    if np.all(grid == Color.BLACK):
        yield []
        return

    for x, y in np.ndindex(grid.shape):
        if grid[x, y] == Color.BLACK:
            continue

        # check if there is an object of the required dimensions
        for w, h in [(2, 2), (3, 1), (1, 3)]:
            if x+w <= grid.shape[0] and y+h <= grid.shape[1]:
                if np.all(grid[x:x+w, y:y+h] != Color.BLACK):
                    new_object = np.zeros_like(grid)
                    new_object[x:x+w, y:y+h] = Color.GREY
                    new_grid = np.copy(grid)
                    new_grid[x:x+w, y:y+h] = Color.BLACK

                    for new_decomposition in search_for_decompositions(new_grid):
                        yield [new_object] + new_decomposition

def main(input_grid: np.ndarray) -> np.ndarray:

    output_grid = np.copy(input_grid)

    for decomposition in search_for_decompositions(input_grid):
        # Check if that decomposition covers the entire grid
        # If it does, then we have found the correct decomposition
        number_of_grey_pixels = sum(np.sum(obj == Color.GREY) for obj in decomposition)
        if number_of_grey_pixels == np.sum(input_grid != Color.BLACK):
            break

    for obj in decomposition:
        w, h = crop(obj).shape

        if w == 2 and h == 2:
            output_grid[obj != Color.BLACK] = Color.TEAL
        elif (w == 3 and h == 1) or (w == 1 and h == 3):
            output_grid[obj != Color.BLACK] = Color.RED
        else:
            assert 0, "Invalid object found"

    return output_grid



def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    n_objects = np.random.randint(4, 8)

    for _ in range(n_objects):
        color = Color.GREY

        w, h = random.choice([(2, 2), (3, 1), (1, 3)])

        # filled with the color
        obj = np.zeros((w, h), dtype=int)
        obj[:w, :h] = color

        # place the object randomly on the grid, assuming we can find a spot
        try:
            x, y = random_free_location_for_object(grid, obj, background=Color.BLACK)
        except:
            continue

        blit(grid, obj, x, y, background=Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)