from common import *
import numpy as np
from typing import *

# concepts:
# pattern alignment, color indicator

# description:
# In the input you will see several objects that each have gray pixel(s) on their left/right side.
# To make the output, move the objects to align their gray pixels. Then change the gray to be the other color of each object. 
# Remove any empty columns.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid for processing
    output_grid = np.copy(input_grid)  

    # Initialize the number of rows in the output grid and a counter for non-empty rows
    m, n = len(output_grid), 0  

    # Identify and count non-empty rows
    for i in range(m):
        flag = True
        for j in range(3):
            if output_grid[i, j] != Color.BLACK:
                flag = False
        if not flag:
            # Increment the counter for non-empty rows
            n += 1  

    # Initialize the output grid with zeros (black color)
    output_grid = np.zeros((n, 3), dtype=int) 

    # x: index for the output grid row, last_x: index for the starting row of the current block, last_y: column index of gray color
    x, last_x, last_y = 0, 0, 0  

    for i in range(m + 1):
        flag = True
        if i < m:
            # Check if the current row is empty
            for j in range(3):
                if output_grid[i, j] != Color.BLACK:
                    flag = False
        if not flag:
            # Copy non-empty rows to the output grid
            for j in range(3):
                output_grid[x, j] = output_grid[i, j]
            x += 1
        elif x > last_x:
            # Process empty rows and align columns
            c, mx, mn = 0, -1, 3
            for k in range(last_x, x):
                for j in range(3):
                    if output_grid[k, j] != Color.BLACK:
                        mx = max(mx, j)
                        mn = min(mn, j)
                    if output_grid[k, j] != Color.BLACK and output_grid[k, j] != Color.GREY:
                        c = output_grid[k, j]
            if last_x > 0:
                offset = 0
                # Determine the offset needed to align columns
                for k in range(-mn, 3 - mx):
                    if last_y - k >= 0 and last_y - k < 3 and output_grid[last_x, last_y - k] == Color.GREY:
                        offset = k
                if offset < 0:
                    # Shift columns left if needed
                    for k in range(last_x, x):
                        for j in range(3):
                            if j - offset < 3:
                                output_grid[k, j] = output_grid[k, j - offset]
                            else:
                                output_grid[k, j] = Color.BLACK
                if offset > 0:
                    # Shift columns right if needed
                    for k in range(last_x, x):
                        for j in range(2, -1, -1):
                            if j - offset >= 0:
                                output_grid[k, j] = output_grid[k, j - offset]
                            else:
                                output_grid[k, j] = Color.BLACK
                output_grid[last_x, last_y] = c
            # Update the column index for gray color
            for j in range(3):
                if output_grid[x - 1, j] == Color.GREY:
                    last_y = j
                    output_grid[x - 1, j] = c
            # Update the starting row index for the next block
            last_x = x 

    return output_grid

def generate_input() -> np.ndarray:
    # Define the initial dimensions of the grid
    n, m = 3, 20  
    # Initialize the grid with zeros (black color)
    grid = np.zeros((n, m), dtype=int) 

    # Exclude gray color for pattern generation
    colors = Color.NOT_BLACK.copy()
    colors.remove(Color.GREY)  
    # Randomly choose the number of patterns to generate
    t = random.choice([3, 4])  
    # Initial starting position for the pattern
    X, Y = random.choice([0, 1, 2]), 0  
    f_h = True

    # Generate color patterns
    while t > 0:
        t -= 1
        # Choose a random color for the pattern
        c = random.choice(colors)  
        x, y = X, Y
        mx, mn = X, X
        f_t = True
        t_in = random.choice([3, 4])

        while t_in > 0:
            t_in -= 1
            if (not f_h and f_t) or (t_in == 0 and t > 0):
                # Mark the position with gray color
                grid[x, y] = Color.GREY 
            else:
                # Set the color at the current position
                grid[x, y] = c  
            f_t = False
            # Possible directions to extend the pattern
            dires = [[0, 1]]  
            if t_in > 0 and x > 0 and grid[x - 1, y] == Color.BLACK:
                dires.append([-1, 0])
            if t_in > 0 and x < 2 and grid[x + 1, y] == Color.BLACK:
                dires.append([1, 0])
            # Choose a random direction to extend the pattern
            dire = random.choice(dires)  
            x += dire[0]
            y += dire[1]
            mx = max(mx, x)
            mn = min(mn, x)

        if not f_h:
            dires = [0]
            # Determine possible shifts for column alignment
            for i in range(1, 3):
                if i <= mn:
                    dires.append(-i)
                if i <= 2 - mx:
                    dires.append(i)
            dire = random.choice(dires)
            if dire < 0:
                # Shift columns left
                for _x in range(3):
                    for _y in range(Y, y):
                        if _x - dire < 3:
                            grid[_x, _y] = grid[_x - dire, _y]
                        else:
                            grid[_x, _y] = Color.BLACK
            if dire > 0:
                # Shift columns right
                for _x in range(2, -1, -1):
                    for _y in range(Y, y):
                        if _x - dire >= 0:
                            grid[_x, _y] = grid[_x - dire, _y]
                        else:
                            grid[_x, _y] = Color.BLACK

        f_h = False
        X, Y = x, y + 1  # Update the starting position for the next pattern
    
    grid_ = np.zeros((n, Y - 1), dtype=int)

    for x in range(n):
        for y in range(Y - 1):
            grid_[x, y] = grid[x, y]

    return grid_.T

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
