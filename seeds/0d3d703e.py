from common import *

import numpy as np
from typing import *

# concepts:
# color mapping

# description:
# The input is a 3x3 grid where each column is of the same color. 
# You will output the corresponding color mapping in a 3x3 grid with each column being the same color. 

def main(input_grid):
    # Initialize output grid
    output_grid = input_grid.copy()

    # Performs color mapping by columns
    for i in range(output_grid.shape[0]):
      output_grid[i] = color_map[output_grid[i,0]]

    return output_grid
    
# Constructing the color map
color_map = {Color.GREEN : Color.YELLOW, 
             Color.BLUE : Color.GRAY, 
             Color.RED : Color.PINK,
             Color.TEAL : Color.MAROON,
             Color.YELLOW : Color.GREEN, 
             Color.GRAY : Color.BLUE, 
             Color.PINK : Color.RED,
             Color.MAROON : Color.TEAL             
            }


def generate_input():
  # Choosing 3 different colors to color the columns that is not orange or black
  color1 = random.choice(list(Color.NOT_BLACK))
  while color1 == Color.ORANGE:
     color1 = random.choice(list(Color.NOT_BLACK))
  color2 = random.choice(list(Color.NOT_BLACK))
  # Check if color 1 and 2 are the same 
  while color1 == color2 or color2 == Color.ORANGE:
     color2 = random.choice(list(Color.NOT_BLACK))
  color3 = random.choice(list(Color.NOT_BLACK))
  # Check if color3 is same as color1 or color2
  while color1==color3 or color2 == color3 or color3 == Color.ORANGE:
     color3 = random.choice(list(Color.NOT_BLACK))

  # Creating the grid 
  grid = np.zeros((3,3), dtype=int)
  grid[0] = color1 
  grid[1] = color2
  grid[2] = color3
  
  return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)