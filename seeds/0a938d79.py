from common import *

import numpy as np
from typing import *

# concepts:
# repetition, horizontal/vertical bars

# description:
# In the input you will see a pair of colored pixels
# Make each pixel into a horizontal/vertical bar by connecting it to the other side of the canvas
# Then, repeat the bars indefinitely in the same direction: either downward (for horizontal bars) or rightward (for vertical bars)

def main(input_grid: np.ndarray) -> np.ndarray:
    # find the individual coloured pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)

    # there should be exactly two colored pixels
    assert len(colored_pixels) == 2

    # find the two pixels
    pixel1, pixel2 = colored_pixels
    x1, y1 = pixel1
    x2, y2 = pixel2
    color1, color2 = input_grid[x1, y1], input_grid[x2, y2]

    # make the horizontal/vertical bars
    output_grid = np.copy(input_grid)

    # check if they should be horizontal (constant y) or vertical (constant x)
    # if they are on the top or bottom, they should be vertical
    if y1 == 0 or y1 == input_grid.shape[1] - 1 or y2 == 0 or y2 == input_grid.shape[1] - 1:
        # vertical bars: constant x
        output_grid[x1, :] = color1
        output_grid[x2, :] = color2

        # repeat the vertical bars indefinitely
        # first, figure out how far apart they are.
        dx = abs(x2 - x1)
        # next, each repetition needs to be separated by twice that amount, because we have two lines
        dx = 2 * dx
        # finally, repeat the vertical bars indefinitely, using the same colors and using a list slice to repeat the bars
        output_grid[x1::dx, :] = color1
        output_grid[x2::dx, :] = color2
    else:
        # horizontal bars: constant y
        output_grid[:, y1] = color1
        output_grid[:, y2] = color2

        # repeat the horizontal bars indefinitely
        # first, figure out how far apart they are.
        dy = abs(y2 - y1)
        # next, each repetition needs to be separated by twice that amount, because we have two lines
        dy = 2 * dy
        # finally, repeat the horizontal bars indefinitely, using the same colors and using a list slice to repeat the bars
        output_grid[:, y1::dy] = color1
        output_grid[:, y2::dy] = color2

    return output_grid



def generate_input() -> np.ndarray:
    # make a grid that is narrow and tall. This is for horizontal lines, and we will flip a coin at the end to transpose everything to make things vertical
    n = np.random.randint(5, 10)
    m = np.random.randint(n+1, 30)
    grid = np.zeros((n, m), dtype=int)

    # place two colored pixels. They should be on the left/right edges, so that they give rise to horizontal bars
    x1, y1, color1 = random.choice([0,n-1]), np.random.randint(m//2), random.choice(Color.NOT_BLACK)
    x2, y2, color2 = random.choice([0,n-1]), np.random.randint(y1+2, m), random.choice(Color.NOT_BLACK)

    grid[x1, y1] = color1
    grid[x2, y2] = color2

    # decide to either do vertical or horizontal
    vertical = np.random.choice([True, False])
    if vertical: 
        # transpose the grid
        grid = grid.T

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)