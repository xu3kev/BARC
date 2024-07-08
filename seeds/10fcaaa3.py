from common import *

import numpy as np
from typing import *

# concepts:
# Coloring diagonal pixels, repetition

# description:
# Given an input grid of arbitrary size, with some small number of colored pixels on it.
# To produce the output, replicate the input grid 4 times, 2 on the top and 2 on the bottom. 
# Color all the diagonal pixels adjacent to a colored pixel teal if the diagonal pixels are black. 

def main(input_grid):
   # Replicate input grid 4 times to initialize output grid
   output_grid = np.zeros((2*input_grid.shape[0], 2* input_grid.shape[1]),dtype=int)
   for i in range(2):
      for j in range(2):
         blit_sprite(output_grid, input_grid, i*input_grid.shape[0], j*input_grid.shape[1])
  
   # Create diagonal directions
   diagonal_dx_dy = [(1,1),(-1,1),(1,-1),(-1,-1)]

   # Color diagonal pixels 
   for y in range(output_grid.shape[1]):
      for x in range(output_grid.shape[0]):
         if output_grid[x,y] != Color.BLACK and output_grid[x,y] != Color.TEAL:
            for dx,dy in diagonal_dx_dy:
               # Color diagonal pixel teal if it is black
               if x+dx >= 0 and x+dx < output_grid.shape[0] and y+dy >= 0 and y+dy < output_grid.shape[1] and output_grid[x+dx,y+dy] == Color.BLACK:
                  output_grid[x+dx,y+dy] = Color.TEAL
  
   return output_grid

def generate_input():
    # Have 1 to 4 number of colored pixels in the initial square
    n_colored_pixels = random.randint(1,4)
    
    # Random pixel color that is not black or teal. 
    pixel_color = random.choice(list(Color.NOT_BLACK))
    while pixel_color == Color.TEAL:
        pixel_color = random.choice(list(Color.NOT_BLACK))

    # Random size of input grid
    n,m= random.randint(2,10), random.randint(2,10)

    # Initialize grid
    grid = np.zeros((n,m),dtype=int)
  
    # Create a dummy sprite with one pixel. 
    sprite = np.array([pixel_color]).reshape(1,1)
    
    # Randomly place n_colored_pixels pixels on the grid
    for i in range(n_colored_pixels):
      x,y = random_free_location_for_sprite(grid,sprite)
      blit_sprite(grid, sprite, x,y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)