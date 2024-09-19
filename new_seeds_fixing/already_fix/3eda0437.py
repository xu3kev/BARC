from common import *
import numpy as np
from typing import *

# concepts:
# rectangle detection

# description:
# In the input you will see a grid with random blue pixels on it.
# To make the output, you should find the largest rectangle area of black cells and turn it into pink.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Output grid is same as input grid except the largest rectangle area of black cells is turned into pink
    output_grid = np.copy(input_grid)

    # Initialize the largest rectangle's position and size
    largest_rec_x, largest_rec_y, largest_rec_len, largest_rec_height = 0, 0, 0, 0 

    # Iterate over each cell in the grid
    # Find the largest black rectangle start from each cell
    for x in range(0, len(output_grid)):
        for y in range(0, len(output_grid[0])):
            # Skip cells with blue color
            if output_grid[x, y] == Color.BLUE:
                continue  
            
            # Initialize the minimum height of the rectangle
            minimum_height = len(output_grid)  

            # Extend the rectangle downward as long as cells are black
            for cur_x in range(x, len(output_grid)):
                if output_grid[cur_x, y] != Color.BLACK:
                    break

                # Extend the rectangle to the right as long as cells are black
                for cur_y in range(y, len(output_grid[0]) + 1):
                    if cur_y == len(output_grid[0]) or output_grid[cur_x, cur_y] != Color.BLACK:
                        # Update the height of the rectangle
                        minimum_height = min(minimum_height, cur_y - y)  
                        break

                # Get the width of founded black rectangle
                maximum_width = cur_x - x + 1

                # Ensure the rectangle is not a line or point
                if maximum_width >= 2 and minimum_height >= 2:
                    # Check if the current rectangle is the largest found so far
                    if largest_rec_len * largest_rec_height < (cur_x - x + 1) * minimum_height:
                        # Update the largest rectangle found so far
                        largest_rec_x, largest_rec_y, largest_rec_len, largest_rec_height = x, y, maximum_width, minimum_height

    # Create a pink sprite with the size of the largest rectangle found
    pink_rectangle = random_sprite(n=largest_rec_len, m=largest_rec_height, color_palette=[Color.PINK], density=1.0)

    # Place the pink sprite on the grid
    blit_sprite(grid=output_grid, sprite=pink_rectangle, x=largest_rec_x, y=largest_rec_y)

    return output_grid

def generate_input() -> np.ndarray:
    # Generate the background grid with size of n x m.
    n, m = np.random.randint(20, 30), np.random.randint(3, 5)
    grid = np.zeros((n, m), dtype=int)

    # Randomlargest_rec_height scatter density of blue color pixels on the grid.
    density = 0.6
    colored = 0
    while colored < density * n * m:
        x = np.random.randint(0, n)
        y = np.random.randint(0, m)
        if grid[x, y] == Color.BLACK:
            grid[x, y] = Color.BLUE
            colored += 1
    
    # Define random size for the pink rectangle, the rectangle should not be a line or point
    rectangle_width = max(2, random.randint(int(0.25 * n), int(0.45 * n)))
    rectangle_height = max(2, random.randint(int(0.5 * m), int(0.75 * m)))

    # The pink rectangle region are represented by color black
    rectangle = random_sprite(n=rectangle_width, m=rectangle_height, color_palette=[Color.BLACK], density=1.0, background=[Color.BLUE])
    
    # Place the pink sprite at a random position in the grid
    pos_x, pos_y = random.randint(0, n - rectangle_width + 1), random.randint(0, m - rectangle_height + 1)
    grid = blit_sprite(grid=grid, sprite=rectangle, x=pos_x, y=pos_y, background=[Color.BLUE])
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)