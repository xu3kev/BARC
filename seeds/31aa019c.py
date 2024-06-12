from common import *

import numpy as np
from typing import *

# concepts:
# counting, uniqueness, surrounding

# description:
# In the input, you will see a grid with 10x10 grid with many colored pixels.
# To make the output, find the cell that is uniquely colored, that is that cell is the only one of that color, then surround that cell with red blocks. Make all the other cells black.

def main(input_grid: np.ndarray) -> np.ndarray:
   #find the index and value of the unique cell
    row=np.size(input_grid,axis=0)
    col = np.size(input_grid,1)
    frequency_dict = {}
    unique = 0
    for i in range(row):
        for j in range(col):
            key = input_grid[i][j]
            if key in frequency_dict:
                frequency_dict[key] +=1
            else:
                frequency_dict[key] = 1
    #find the value of the unique cell
    for key in frequency_dict:
        freq = frequency_dict[key]
        if freq == 1:
            unique = key
    #find index
    result = np.where(input_grid == unique)
    row_index, col_index = result[0][0], result[1][0]
    
    #create output grid
    output_grid = np.zeros((row,col), dtype=int)
    #set the neighbors to the RED color
    for i in range(row_index - 1, row_index + 2):
        for j in range(col_index - 1, col_index + 2):
            output_grid[i][j]=Color.RED
    #set the cell to be the unique color
    output_grid[row_index][col_index] = unique
    return output_grid
    



def generate_input() -> np.ndarray:
    
    # make a 10x10 black grid first as background
    n, m = 10, 10
    matrix = np.zeros((n, m), dtype=int)

    #randomly select a unique color from Color.NOT_BLACK
    unique_color = random.choice(Color.NOT_BLACK)

    #randomly choose a non-border cell for the unique color
    non_border_cells = [(i, j) for i in range(1, 9) for j in range(1, 9)]
    unique_cell = random.choice(non_border_cells)
    matrix[unique_cell] = unique_color

    #remove the unique color from the list
    remaining_colors = [color for color in Color.NOT_BLACK if color != unique_color]

    #generate frequencies for the remaining non-unique colors
    frequencies = []
    total_cells = 0
    #ensures that there are between 20 and 40 cells colored
    while total_cells < 20 or total_cells > 40:
        frequencies = [random.choice([0, 2, 3, 4, 5, 6]) for _ in range(8)]
        total_cells = sum(frequencies)
        
    #assign the remaining colors to the matrix
    color_cells = []
    for color, freq in zip(remaining_colors, frequencies):
        color_cells.extend([color] * freq)

    random.shuffle(color_cells)

    #place colors in the matrix, avoiding the unique cell
    available_cells = [(i, j) for i in range(10) for j in range(10) if (i, j) != unique_cell]
    random.shuffle(available_cells)
    #randomly assigning the avialble cells to their color
    for cell, color in zip(available_cells, color_cells):
        matrix[cell] = color
    return matrix
  



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)