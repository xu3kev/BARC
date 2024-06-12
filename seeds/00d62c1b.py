from common import *

import numpy as np
from typing import *

# concepts:
# floodfill, detecting enclosed regions. 

# description:
# The input grid is a square grid with black and green pixels. The input grid should have regions that are enclosed by the green pixels. 
# To produce the output, you need to find the enclosed regions in the input grid, and then color them yellow. 
                
def main(input_grid):
    # Create initial output grid template based on input grid.
    output_grid = input_grid.copy()

    # Find enclosed regions
    enclosed_regions = find_enclosed_region(input_grid)

    # Color enclosed regions
    for (x,y) in enclosed_regions:
        flood_fill(output_grid,x,y,Color.YELLOW)

    return output_grid

def find_enclosed_region(grid):
    # Returns a list of (x,y) coordinates for one pixel in each enclosed region, or return [] if there are no enclosed regions. 
    # The idea used is to floodfill every not visited pixel, and then check if it bleeds to an edge. 
    # If it did, then none of the floodfilled pixels are in an enclosed region. Mark floodfilled pixels as visited. 
    
    # Creates a grid that keeps track of which pixels are visited during floodfill. 
    visited_pixels = grid.copy()
    visited_color = Color.BLUE

    # output pixel list
    pixels_of_enclosed = []

    # Check for enclosed region and add to pixels_of_enclosed if there is one. 
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            
            # Only need to check black pixels
            if visited_pixels[x,y] == Color.BLACK:
                # Track all pixels that will be visited at this floodfill iteration
                flood_fill(visited_pixels, x, y, visited_color)

                # Test for enclosed region
                temp_grid = grid.copy()
                flood_fill(temp_grid, x,y, visited_color)
                # If any of the edge pixel is of the floodfilled color, then it is not enclosed.
                if (np.sum(temp_grid[0,:] == visited_color) == 0) and (np.sum(temp_grid[-1,:] == visited_color) == 0) and (np.sum(temp_grid[:,0] == visited_color) == 0) and (np.sum(temp_grid[:,-1] == visited_color) == 0):
                    pixels_of_enclosed.append((x,y))

    return pixels_of_enclosed 

def generate_input():
    # Generate a square grid of arbitrary size with black background, size from 5x5 to 20x20
    n = random.randint(5, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate a random sprite
    grid = random_sprite(n,n,color_palette=[Color.GREEN])

    # Check to make sure we generated a grid with enclosed regions
    while find_enclosed_region(grid) == []:
        grid = generate_input()
    
    return grid 

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
