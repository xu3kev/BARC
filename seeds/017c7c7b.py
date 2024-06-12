from common import *

import numpy as np
from typing import *

# concepts:
# Detecting and copying repeating patterns

# description:
# In the input you will see a 6x3 grid repeating a nx3 pattern. 
# In the output, you want to repeat the same pattern on a 9x3 grid. 
 
def main(input_grid):
    # Initialize output grid
    output_grid = np.zeros((3,9),dtype=int)

    # Detecting patterns in the input grid
    num_pattern_rows = 0
    # Checking 1 row case
    n1 = True 
    for i in range(1,input_grid.shape[1]):
        if not np.equal(input_grid[:,0], input_grid[:,i]).all():
            n1 = False
            break
    if n1:
        num_pattern_rows = 1 
    # Checking 2 row case
    elif np.equal(input_grid[: ,0:2], input_grid[:,2:4]).all() and np.equal(input_grid[: ,2:4], input_grid[:,4:6]).all():
        num_pattern_rows = 2
    # Checking 3 row case
    elif np.equal(input_grid[: ,0:3], input_grid[:,3:6]).all():
        num_pattern_rows = 3
    # Checking 4 row case
    elif np.equal(input_grid[: ,0:2], input_grid[:,4:6]).all():
        num_pattern_rows = 4
    # Checking 5 row case
    elif np.equal(input_grid[: ,0], input_grid[:,5]).all():
        num_pattern_rows = 5
    # Else 6 row case
    else:
        num_pattern_rows = 6 

    # Recognizing pattern in input grid and changes its color
    sprite = input_grid[:, 0:num_pattern_rows]
    sprite[sprite==Color.BLUE] = Color.RED

    # Copying pattern
    repeat_pattern(output_grid,sprite)

    return output_grid

def repeat_pattern(grid,sprite):
    # Copy sprite to fill the entire grid
    for i in range(0, grid.shape[1], sprite.shape[1]):
        if i+sprite.shape[1] <= grid.shape[1]:
          blit(grid, sprite,0,i)
        else:
          blit(grid, sprite[:,0:grid.shape[1]-i],0,i)

def generate_input():
    # Choose a random color
    color = Color.BLUE

    # Creates a random smaller sprite, where the number of row is chosen randomly from 3 or 4
    row = random.randint(3,4)

    # if not 3x3, then cannot be diagonal symmetry 
    if row == 3:
        sprite = random_sprite(3,row,color_palette=[color])
    else:
        symmetry = random.choice(['horizontal', 'vertical', 'not_symmetric'])
        sprite = random_sprite(3,row, symmetry=symmetry, color_palette=[color])

    # Creates grid and lay the smaller pattern inside
    grid = np.zeros((3,6),dtype = int)

    # Repeatedly copies pattern until reaching the end
    repeat_pattern(grid,sprite)

    return grid 

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)