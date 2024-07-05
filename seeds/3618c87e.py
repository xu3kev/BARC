from common import *

import numpy as np
from typing import *

# concepts:
# color, falling

# description:
# In the input, you should see a gray baseline at the bottom. For each gray baseline pixel, there may or may not be gray pixels above it. If there are gray pixels above it, you can see a blue pixel above the gray pixels.
# To make the output, make the blue pixels fall downward, falling through the gray baseline until they hit the bottom.

def main(input_grid):
    output_grid = np.copy(input_grid)

    width, height = output_grid.shape

    # Find the color of the bottom baseline
    baseline = output_grid[:, -1]
    baseline_colors = np.unique(baseline)
    assert len(baseline_colors) == 1
    baseline_color = baseline_colors[0]

    # Find the color of the background, which is the most common color
    background_color = np.argmax(np.bincount(output_grid.flatten()))

    # Now make all the other colors fall down
    for x in range(width):
      for y in range(height):
          if output_grid[x, y] != background_color and output_grid[x, y] != baseline_color:
              # Make it fall to the bottom
              # Do this by finding the background/baseline spot below it which is closest to the bottom
              possible_y_values = [ possible_y for possible_y in range(y+1, height)
                                   if output_grid[x, possible_y] == background_color or output_grid[x, possible_y] == baseline_color]
              if len(possible_y_values) > 0:
                  closest_to_bottom_y = max(possible_y_values)
                  output_grid[x, closest_to_bottom_y] = output_grid[x, y]
                  output_grid[x, y] = background_color                  
  
    return output_grid


def generate_input():
    width, height = 5, 5
    input_grid = np.zeros((width,height), dtype= int)

    # make the bottom pixels gray
    input_grid[:, height-1] = Color.GRAY

    # randomly select 1 or 2 squares
    num_blue_squares = random.choice([1, 2])

    # randomly pick where to put them
    blue_x_positions = random.sample(range(width), num_blue_squares)

    # put the blue squares above new gray squares
    for pos in blue_x_positions:
        # grey is directly above the bottom (directly above height-1)
        input_grid[pos, height-2] = Color.GREY
        # and blue is directly above that
        input_grid[pos, height-3] = Color.BLUE

    return input_grid    



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)