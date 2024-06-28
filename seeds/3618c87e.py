from common import *

import numpy as np
from typing import *

# concepts:
# color, falling

# description:
# In the input, you should see a gray baseline at the bottom, and above each gray cell, there may or may not be gray pixels. If there are gray pixels, you can see a single blue pixel above it.
# To make the output, replace any gray baseline with a blue square above it with the blue square, coloring the spot where the original blue square was black. Alternatively, take the blue squares and place them two squares down.

def main(input_grid):
    
    output_grid = np.copy(input_grid)

    rows, cols = output_grid.shape

    # to generalize this problem to another problem with differnent colors, we solve the problem by counting the frequency of each color in the input grid and letting the least frequent color be the color that we want to replace with another color
    # color to be blue in our example, and the baseline to be the second least frequent color in the input grid 
    color_frequency_dict = {}
    
    for x in range(rows):
      for y in range(cols):
        key = input_grid[x][y]
        if key in color_frequency_dict:
          color_frequency_dict[key] += 1
        else:
          color_frequency_dict[key] = 1

    # Find the color that is the least frequent   
    least_frequent_color = min(color_frequency_dict, key=color_frequency_dict.get)         
    
    # Find the color that is the second least frequent
    color_frequency_dict.pop(least_frequent_color)
    baseline_color = min(color_frequency_dict, key=color_frequency_dict.get)
    
    for x in range(rows):
      for y in range(cols-2):
            # checks that the square is least_frequently occuring color and the square all the way to the right is the baseline color
            
            if output_grid[x, y] == least_frequent_color and output_grid[x, -1] == baseline_color:
                # replace the gray square with the least frequent color square
                output_grid[x, -1] =least_frequent_color
                # replace the blue square with a black square
                output_grid[x, y] = Color.BLACK
  
    return output_grid


def generate_input():
    
    rows, cols = 5,5
    input_grid = np.zeros((rows,cols), dtype= int)

    # make the last column gray
    input_grid[:,cols-1] = Color.GRAY


    # randomly select 1 or 2 squares in the column two to the left of the last to be blue squares 
    num_blue_squares = random.choice([1, 2])
    blue_positions = random.sample(range(cols), num_blue_squares)
    for pos in blue_positions:
        input_grid[pos, cols-3] = Color.BLUE

    # connect the blue squares to the last gray column with gray cells
    for pos in blue_positions:
        input_grid[pos, cols-2] = Color.GRAY
      

    return input_grid    



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)