from common import *

import numpy as np
from typing import *

# concepts:
# Separating pattern repetitions

# description:
# In the input, you will receive 3 repetitions of a square sprite laid horizontally right next to each other. 
# In the output, you want to identify the pattern. 

def main(input_grid):
    # Extract 1/3 of the input grid and return 
    return input_grid[0:int(input_grid.shape[0]/3),:].copy()
    

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