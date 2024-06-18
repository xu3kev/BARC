from common import *

import numpy as np
from typing import *

# concepts:
# Making sprite symmetric, detecting sprite

# description:
# In the input you will see a grid. Within it, there is a smaller nxm grid (n,m odd) that contains 4 parts that are 
# mostly radially symmetric to its center, except for some pixels. Some corresponding parts of these pixels are missing in other quadrants. 
# The output would find the not symmetric pixels and recover its corresponding parts such that the inner grid has radial symmetry.  

def main(input_grid):
    output_grid = input_grid.copy()

    # Finds sprite
    sprite = crop(input_grid.copy())

    # Find the different regions of the sprite
    center_x, center_y = sprite.shape[0]//2+1, sprite.shape[1]//2+1
    upper_left = sprite[0:center_x,0:center_y]
    upper_right = sprite[center_x-1:,0:center_y]
    lower_left = sprite[0:center_x,center_y-1:]
    lower_right = sprite[center_x-1:,center_y-1:]
    # Stores the amount of rotation needed and the regions
    regions = [(upper_left,0),(upper_right,3),(lower_left,1),(lower_right,2)]

    # Make each region have matching pixels from other regions 
    for i in range(len(regions)):
        region_i = np.rot90(regions[i][0],regions[i][1])
        for j in range(len(regions)):
            # Calculate the difference between the regions, only taking into account 
            # the positive values since those are the pixels that the current quadrant is missing
            region_j = np.rot90(regions[j][0].copy(),regions[j][1])
            diff = region_j - region_i
            diff[diff <0 ] = 0
            # Add missing pixels
            region_i+= diff
        regions[i] = (np.rot90(region_i,-regions[i][1]),regions[i][1])
        
    # Create output sprite by combining quadrants
    output_sprite = np.zeros((sprite.shape[0],sprite.shape[1]),dtype=int)
    blit(output_sprite,regions[0][0],0,0)
    blit(output_sprite,regions[1][0],center_x-1,0)
    blit(output_sprite,regions[2][0],0,center_y-1)
    blit(output_sprite,regions[3][0],center_x-1,center_y-1)

    # Place the output sprite back to the output grid
    x,y,_,_ = bounding_box(input_grid)
    blit(output_grid,output_sprite,x,y)

    return output_grid


def generate_input():
    # Initialize 10x10 grid 
    grid = np.zeros((10,10),dtype=int) 

    # Create 5x5 sprite 
    sprite = np.zeros((5,5),dtype=int)
    # Split the points into three classes based on symmetry
    color1 = random.choice(list(Color.NOT_BLACK))
    color2 = random.choice(list(Color.NOT_BLACK))
    color3 = random.choice(list(Color.NOT_BLACK))
    # Color of the center 
    color4 = random.choice(list(Color.NOT_BLACK))

    # Color a radial symemtric sprite that satisfies requirements first. 
    # Corner class
    sprite[0,0] = sprite[0,-1] = sprite[-1,0] = sprite[-1,-1] = color1
    # Cross class
    sprite[0,2] = sprite[2,0] = sprite[-1,2] = sprite[2,-1] = color2
    # Inner class
    sprite[1,1] = sprite[1,3] = sprite[3,1] = sprite[3,3] = color3
    # Center
    sprite[2,2] = color4
    
    # There are only four possible pixels to remove its symmetric components in the upperleft square. 
    # Randomly choose of them and remove corresponding parts
    n = random.randint(0,3)
    # Case 1: remove other corners
    if n==0: 
        sprite[0,-1] = sprite[-1,0] = sprite[-1,-1] = Color.BLACK
    # Case 2: remove other cross
    if n==1:
        sprite[2,0] = sprite[-1,2] = sprite[2,-1] = Color.BLACK
    # Case 3: remove other cross (keeping a different pixel)
    if n==2:
        sprite[0,2] = sprite[-1,2] = sprite[2,-1] = Color.BLACK
    # Case 4: remove other inner corners
    if n==3:
        sprite[1,3] = sprite[3,1] = sprite[3,3] = Color.BLACK 

    # Place sprite randomly onto the grid 
    x,y = random_free_location_for_object(grid, sprite)
    blit(grid,sprite,x,y)

    return grid
    
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)