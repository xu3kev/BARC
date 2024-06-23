from common import *


import numpy as np
from typing import *

# concepts:
# alignment, sliding objects

# description:
# In the input, you should see a black grid with nine 3x3 grey squares randomly placed in it (some of the squares touch a little bit). Each square contains a colored object of a different color, 3-4 cells in area, except for one which is blank. The colored objects are at the border of the 3x3 shape.
# To make the output, create a 9x9 grey grid. Now place each of the 3x3 squares from the input grid into the output grid. The location of an object is done so that the colored object in the grey square is moved "away" fromm the center square of the output grid in the direction the colored object is in the 3x3 square.

def main(input_grid):
    # Plan:
    # 1. Extract the 3x3 grey squares from the input grid (tricky because sometimes they touch)
    # 2. Create the output grid
    # 3. Place the 3x3 squares into the output grid by sliding it in the direction of the colored (non-grey) portion

    # step 1: extract the 3x3 grey squares from the input grid.
    # the grey squares might be connected with 4-way connectivity, so we can't use find_connected_components to extract the squares.
    # instead, we can seach over all locations and extract when the 3x3 square has no black squares at that location.
    n, m = input_grid.shape
    square_length = 3
    squares = []
    for x in range(n-square_length+1):
        for y in range(m-square_length+1):
            square = input_grid[x:x+square_length, y:y+square_length]
            if np.all(square != Color.BLACK):
                squares.append(square)

    assert len(squares) == 9, "There should be exactly 9 3x3 grey squares in the input grid"

    # step 2: create the output grid, which is all grey
    output_grid = np.full((9, 9), Color.GREY, dtype=int)

    # step 3: place the 3x3 squares into the output grid
    # for each square, find the "direction" of the colored object in it, and place it in that direction of the output grid.

    # we can ignore the blank square, since the middle is already grey
    squares = [square for square in squares if not (square == Color.GREY).all()]

    def get_direction_between(point1, point2):
        '''
        returns one of (-1, -1), (-1, 0), (-1, 1),
                       (0, -1), (0, 0), (0, 1),
                       (1, -1), (1, 0), (1, 1)

        based on the direction from point1 to point2
        '''
        x1, y1 = point1
        x2, y2 = point2

        dx, dy = x2 - x1, y2 - y1

        def sign(x):
            if x < 0:
                return -1
            elif x > 0:
                return 1
            else:
                return 0

        return (sign(dx), sign(dy))

    for square in squares:
        colored_object_center_of_mass = np.argwhere(square != Color.GREY).mean(axis=0)
        grey_center_of_mass = np.argwhere(square == Color.GREY).mean(axis=0)

        direction = get_direction_between(grey_center_of_mass, colored_object_center_of_mass)

        # place the square in the middle of the output grid, and then move it in the direction until reaching a border
        x, y = 3, 3
        while 0 < x < 9 - 3 and 0 < y < 9 - 3:
            x += direction[0]
            y += direction[1]

        blit(output_grid, square, x, y)

    return output_grid


def generate_input():

    # 1. create nine 3x3 grey squares with colored objects in them.
    # One is blank. Each of the 8 shapes can be defined by taking a border point, and coloring it and its 4-connected neighbors in a random color.
    squares = []
    for x in range(3):
        for y in range(3):
            square = np.full((3, 3), Color.GREY, dtype=int)

            # Middle square is all grey (blank square)
            if (x, y) == (1, 1):
                squares.append(square)
                continue

            # color this point and its neighbors in a random color
            color = np.random.choice([c for c in Color.ALL_COLORS if c != Color.GREY and c != Color.BLACK])
            square[x, y] = color
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 3 and 0 <= ny < 3:
                    square[nx, ny] = color

            squares.append(square)

    # 2. place the squares randomly in the grid.
    # to do so, we can put each square in a random open location greedily.
    # placement might fail if there is no open location for a square.
    # so try repeatedly until we succeed
    while True:
        # create a black (14-17)x(14-17) grid
        n = np.random.randint(14, 18)
        m = np.random.randint(14, 18)
        input_grid = np.full((n, m), Color.BLACK, dtype=int)
        success = True
        for square in squares:
            try:
                x, y = random_free_location_for_object(input_grid, square, padding=1, padding_connectivity=4)
                blit(input_grid, square, x, y)
            except: # no free location
                success = False
                break

        if success:
            return input_grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
