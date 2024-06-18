from common import *

import numpy as np
from typing import *

# concepts:
# repetition, reflection

# description:
# In the input, you will receive some repetitions and reflections (the first occurence
# is guaranteed not a reflection) of a sprite laid horizontally right next to each other. 
# In the output, you want to identify the sprite. 

def main(input_grid):
    # Initialize output grid
    sprite = input_grid.copy()

    # Detecting patterns in the input grid
    for num_pattern_cols in range(1,input_grid.shape[0]):
        if input_grid.shape[0] % num_pattern_cols == 0:
            # Check complete repeating patterns
            check = True
            for i in range(num_pattern_cols, input_grid.shape[0],num_pattern_cols):
                if i+num_pattern_cols <= input_grid.shape[0] and not np.equal(input_grid[0:num_pattern_cols,:], input_grid[i:i+num_pattern_cols,:]).all() and not np.equal(input_grid[0:num_pattern_cols,:], np.flip(input_grid[i:i+num_pattern_cols,:],axis = 1)).all():
                    check = False 
                
        if check:
            # Recognizing pattern in input grid and changes its color
            sprite = input_grid[0:num_pattern_cols]
          
            return sprite
        
    return sprite

def generate_input():
    # Create the sprite to be duplicated
    n = random.randint(2,7)
    sprite = random_sprite(n,n,color_palette=random.sample(list(Color.NOT_BLACK),3))
    
    # Duplicate the sprite 3 times horizontally
    grid = np.zeros((3*n,n),dtype=int)
    for i in range(3):
        blit(grid, sprite, i*n,0)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)