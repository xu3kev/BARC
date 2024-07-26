from common import *

import numpy as np
from typing import *

# concepts:
# color guide, connectivity, falling

# description:
# In the input grid, you will see several columns with different heights formed by stacking colored pixels on a black background. Each column is separated by at least
# one column of black pixels. All columns except one have the same color. The goal is to find the column that has a different color and shift it down until it 
# touches the bottom of the grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # find all the columns in the input grid
    width, height = input_grid.shape
    columns = []
    for x in range(width):
        if np.any(input_grid[x, :] != Color.BLACK):
            column = input_grid[x, :]
            columns.append((x, column))
    
    # find the column with a different color
    colors = [np.unique(column[column != Color.BLACK])[0] for _, column in columns]
    unique_color = None
    for color in colors:
        if colors.count(color) == 1:
            unique_color = color
            break
    
    # find the unique column and its position
    unique_column, unique_position = None, None
    for pos, (x, column) in enumerate(columns):
        if np.unique(column[column != Color.BLACK])[0] == unique_color:
            unique_column, unique_position = column, pos
            break
    
    # prepare the output grid by copying the input grid
    output_grid = np.copy(input_grid)
    
    # find how low we need to shift the unique column
    non_black_indices = np.argwhere(unique_column != Color.BLACK)
    max_non_black_idx = non_black_indices.max() if len(non_black_indices) > 0 else -1  # -1 if the column is fully black
    
    shift_amount = height - (max_non_black_idx + 1)
    
    # shift the unique column down
    new_column = np.full_like(unique_column, Color.BLACK)
    new_column[shift_amount:] = unique_column[:height - shift_amount]
    
    # place the new column in the respective position
    output_grid[:, columns[unique_position][0]] = new_column
    
    return output_grid

def generate_input() -> np.ndarray:
    # define the size of the grid
    width, height = np.random.randint(10, 15), np.random.randint(10, 15)
    
    # initialize a black grid
    grid = np.full((width, height), Color.BLACK)
    
    # choose a common color and a unique color for the columns
    common_color, unique_color = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)
    
    num_columns = np.random.randint(3, min(6, width // 2))
    
    # generate columns and place them on the grid, ensuring they are separated by at least one black column
    column_positions = np.random.choice(range(width), num_columns, replace=False)
    
    for i, col_pos in enumerate(sorted(column_positions)):
        column_color = unique_color if i == 0 else common_color  # make sure only one column has the unique color
        column_height = np.random.randint(2, height)
        
        for j in range(column_height):
            grid[col_pos, j] = column_color
    
    return grid