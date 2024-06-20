from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines

# description:
# In the input, you will see a horizontal grey line on a black background, with red and blue pixels scattered on either side of the line.
# To make the output, draw vertical lines from each of the blue and red pixels, with lines from the red pixels going toward the grey line and lines from the blue pixels going away from the grey line. 
# These lines should stop when they hit the grey line or the edge of the grid.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the location of the horizontal grey line
    grey_line = np.where(output_grid == Color.GREY)

    # get the unique y-coordinates of the grey line
    grey_line_y = np.unique(grey_line[1])

    # find the red and blue pixels
    red_pixels = np.where(output_grid == Color.RED)
    blue_pixels = np.where(output_grid == Color.BLUE)

    # draw lines from the red pixels toward the grey line
    for i in range(len(red_pixels[0])):
        x, y = red_pixels[0][i], red_pixels[1][i]
        # make sure to handle the case where the red pixel is below the grey line and the case where it is above
        if y < grey_line_y:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, 1), stop_at_color=[Color.GREY])
        else:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, -1), stop_at_color=[Color.GREY])

    # draw lines from the blue pixels away from the grey line, using draw_line
    for i in range(len(blue_pixels[0])):
        x, y = blue_pixels[0][i], blue_pixels[1][i]
        # make sure to handle the case where the blue pixel is below the grey line and the case where it is above
        if y < grey_line_y:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, -1), stop_at_color=[Color.GREY])
        else:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, 1), stop_at_color=[Color.GREY])

    return output_grid

def generate_input():
    # make a 10x10 black grid for the background
    n = m = 10
    grid = np.zeros((n,m), dtype=int)

    # make a horizontal grey line on a random row about halfway down the grid
    row = np.random.randint(m//3, 2*(m//3))
    grid[:, row] = Color.GREY

    # scatter a random number of blue and red pixels on either side of the grey line so that no pixel is in the same column as any other pixel on its side of the grey line
    # select columns for the pixels above the grey line
    cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
    for col in cols:
      # randomly choose whether to make the pixel red or blue
      if np.random.rand() < 0.5:
        grid[col, np.random.randint(row-1)] = Color.RED
      else:
        grid[col, np.random.randint(row-1)] = Color.BLUE
    # select columns for the pixels below the grey line
    cols = np.random.choice(np.arange(m), size=np.random.randint(3, 7), replace=False)
    for col in cols:
      # randomly choose whether to make the pixel red or blue
      if np.random.rand() < 0.5:
        grid[col, np.random.randint(row+1, m)] = Color.RED
      else:
        grid[col, np.random.randint(row+1, m)] = Color.BLUE 
    
    return grid




# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)