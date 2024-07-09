from common import *

import numpy as np
from typing import *

# concepts:
# repeating patterns, colors as indicators, scaling

# description:
# In the input you will see a nxm sprite with black background. 
# Construct an output grid with n^2 x m^2 black pixels. Divide the output grid into subgrids, 
# and look at the corresponding pixel in the nxm input grid. If the corresponding pixel is not black, 
# then copy the nxm input grid into the subgrid. Else, the subgrid does not change. 

def main(input_grid):
    # creates an empty 9x9 output grid 
    output_grid = np.zeros((input_grid.shape[0]**2,input_grid.shape[1]**2),dtype=int)

    input_sprite = input_grid

    # Go through the input grid. If an input grid pixel is not black, 
    # then copy the input grid to the corresponding location on the output grid
    for n in range(input_grid.shape[0]):
      for m in range(input_grid.shape[1]):
        if input_grid[n,m] != Color.BLACK:
            blit_sprite(output_grid, input_sprite, n*input_grid.shape[0], m*input_grid.shape[1])
    
    return output_grid

def generate_input():
  n,m = random.randint(3, 6), random.randint(3, 6)
  random_color = random.choice(list(Color.NOT_BLACK))
  return random_sprite(n, m, color_palette=[random_color])


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)