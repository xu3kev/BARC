from common import *

import numpy as np
from typing import *

# concepts:
# Detecting and copying repeating patterns

# description:
# In the input you will see a nxm grid repeating a kxm pattern. 
# In the output, you want to repeat the same pattern on a 9xm grid. 
 
def main(input_grid):
    # Initialize output grid
    output_grid = np.zeros((input_grid.shape[0],9),dtype=int)

    # Detecting patterns in the input grid
    for num_pattern_rows in range(1,input_grid.shape[1]):
        # Check complete repeating patterns
        check = True
        for i in range(num_pattern_rows, input_grid.shape[1],num_pattern_rows):
            if i+num_pattern_rows <= input_grid.shape[1] and not np.equal(input_grid[:,0:num_pattern_rows], input_grid[:,i:i+num_pattern_rows]).all():
                check = False 
                
        # Check last few rows (potentially not complete pattern)
        num_remaining_rows = input_grid.shape[1] % num_pattern_rows
        if check and num_remaining_rows != 0 :
            if not np.equal(input_grid[:,0:num_remaining_rows], input_grid[:, -1*num_remaining_rows:]).all():
                check = False
        if check:
            
            # Recognizing pattern in input grid and changes its color
            sprite = input_grid[:, 0:num_pattern_rows]
            sprite[sprite==Color.BLUE] = Color.RED

            # Copying pattern
            repeat_pattern(output_grid,sprite)

            return output_grid
        
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
    row = random.randint(4,4)

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