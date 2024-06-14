from common import *

import numpy as np
from typing import *

# concepts:
# Identifying area separated by lines. 

# description:
# In the input, you will be given a square grid with some non-consecutive horizontal and vertical lines. 
# In the output, you want to identify the number of areas separated by these lines and put them into a grid. 
# For example, if the grid is horizontally separated into n areas and vertically separated into m areas, then output 
# a nxm grid. 
def main(input_grid):
    # Count number of area separated in the first row
    background = input_grid[0,0]
    n_vertical_lines = 1
    for x in range(input_grid.shape[0]):
        if input_grid[x,0]!= background:
            n_vertical_lines+=1
    
    # Count number of area separated in the first column 
    n_horizontal_lines = 1
    for y in range(input_grid.shape[1]):
        if input_grid[0,y]!= background:
            n_horizontal_lines+=1

    # Create output grid 
    output_grid = np.full((n_vertical_lines,n_horizontal_lines),background, dtype=int)
    
    return output_grid

def generate_input():
    # Picking background and line colors
    background = random.choice(list(Color.NOT_BLACK))
    lines = random.choice(list(Color.NOT_BLACK))
    # Check lines and background are not the same
    while lines == background:
        lines = random.choice(list(Color.NOT_BLACK))

    # Creating the background grid
    n= random.randint(10,20)
    grid = np.full((n,n),background, dtype=int)

    # Picking how many lines to have in each dimension
    line_n, line_m = random.randint(0, n // 3), random.randint(0, n // 3)

    # Draw vertical lines (except endpoints)
    possible_index = np.arange(1, n-1, 1)
    for i in range(line_n):
        draw_ind = random.choice(list(possible_index)) 
        draw_line(grid, draw_ind, 0,n,lines,(0,1))
        possible_index = possible_index[(possible_index!=draw_ind) & (possible_index!=draw_ind+1) & (possible_index!=draw_ind-1) ]
    
    # Draw horizontal lines (except endpoints)
    possible_index = np.arange(1, n-1, 1)
    for i in range(line_m):
        draw_ind = random.choice(list(possible_index)) 
        draw_line(grid, 0,draw_ind,n,lines,(1,0))
        possible_index = possible_index[(possible_index!=draw_ind) & (possible_index!=draw_ind+1) & (possible_index!=draw_ind-1) ]
    
    return grid 



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)