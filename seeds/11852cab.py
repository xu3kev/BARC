from common import *

import numpy as np
from typing import *

# concepts:
# Making sprite symmetric, detecting sprite

# description:
# In the input you will see a 10x10 grid. Within it, there is a 5x5 grid that contains 4 parts that are 
# mostly radially symmetric to the center of the 5x5, except for one pixel. This pixel only appears in the 
# upper left section of the 5x5 grid and its corresponding parts for the other three quadrants are missing. 
# If the 5x5 grid were radially symmetric, exactly every other pixel would be colored, starting with the pixels 
# at the corner being colored. 
# The output would find the not symmetric pixel and recover its corresponding parts such that the 5x5 grid has radial symmetry.  

def main(input_grid):
    output_grid = input_grid.copy()

    # Finds sprite and color missing pieces
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x,y] != Color.BLACK:
                # Check which of the cross pixel in upper left is colored
                cross_color = output_grid[x,y+2] if output_grid[x,y+2] != Color.BLACK else output_grid[x+2,y]
                # Re-color
                make_radial_symmetry(output_grid[x:x+5,y:y+5], output_grid[x,y], cross_color, output_grid[x+1,y+1], output_grid[x+2,y+2])     
                return output_grid
            
    return output_grid

def make_radial_symmetry(sprite, color1, color2, color3, color4):
    # Color a radial symmetric grid where every other pixel is black.  
    # Modifies in place

    # Corner class
    sprite[0,0] = sprite[0,-1] = sprite[-1,0] = sprite[-1,-1] = color1
    # Cross class
    sprite[0,2] = sprite[2,0] = sprite[-1,2] = sprite[2,-1] = color2
    # Inner class
    sprite[1,1] = sprite[1,3] = sprite[3,1] = sprite[3,3] = color3
    # Center
    sprite[2,2] = color4

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
    make_radial_symmetry(sprite, color1, color2, color3, color4)

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