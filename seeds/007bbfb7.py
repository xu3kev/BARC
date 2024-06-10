from common import *

import numpy as np
from typing import *

# concepts:
# repeating patterns, colors as indicators, scaling

# description:
# In the input you will see a 3x3 sprite with black background. 
# Construct a 9x9 output grid with black pixels. Divide the 9x9 output grid into nine 3x3 subgrids, 
# and look at the corresponding pixel in the 3x3 input grid. If the corresponding pixel is not black, 
# then copy the 3x3 input grid into the 3x3 subgrid. Else, the subgrid does not change. 

def main(input_grid):
    # creates an empty 9x9 output grid 
    output_grid = np.zeros((9,9),dtype=int)

    # Go through the input grid. If an input grid pixel is not black, 
    # then copy the input grid to the corresponding location on the output grid
    for n in range(input_grid.shape[0]):
      for m in range(input_grid.shape[1]):
        if input_grid[n,m] != Color.BLACK:
            blit(output_grid, input_grid, n*3, m*3)
    
    return output_grid

# creates a random 3x3 grid with black background and some pixels of another color. 
def generate_input():
  random_color = random.choice(Color.NOT_BLACK)
  return random_sprite(3, 3, color_palette=[Color.BLACK, random_color])


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)