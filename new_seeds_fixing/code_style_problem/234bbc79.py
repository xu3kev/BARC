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
    grid_width, grid_height = input_grid.shape

    # Get the final width of the output grid, which remove empty columns
    final_width = np.any(input_grid != 0, axis=1).sum()

    # Initialize the output grid with zeros (black color)
    output_grid = np.zeros((final_width, grid_height), dtype=int)
    # Create a copy of the input grid for processing 
    grid = np.copy(input_grid)

    # Extract the colored objects and their boundary from grid
    objects = detect_objects(grid = grid, connectivity = 4)
    object_boundary = [bounding_box(grid = x) for x in objects]

    # Sort the objects according the x_min of each object
    object_boundary, objects = zip(*sorted(zip(object_boundary, objects), key=lambda x: x[0]))
    object_boundary, objects = list(object_boundary), list(objects)
    object_number = len(objects)

    # Initialize the processed width and the y-axis of the rightest gray grid
    process_width, pre_right_gray_posy = 0, 0

    # Handle each object
    for i in range(object_number):
        # Extract the boundary of the i-th object
        x_min, y_min, x_length, y_length = object_boundary[i]
        x_max, y_max = x_min + x_length - 1, y_min + y_length - 1
        pos_x_min, pos_y_min, pos_x_max, pos_y_max = process_width, y_min, process_width + x_length - 1, y_max
        color = [x for sublist in objects[i] for x in sublist if x != Color.BLACK and x != Color.GREY][0]

        # For each object except the first one, the grey grid in it should match the gray grid of the last one, 
        #   and change the color from grey to the object's color
        if i > 0:
            for move in range(-y_min, grid_height - y_max):
                move_gray_posy = pre_right_gray_posy - move
                if move_gray_posy >= 0 and move_gray_posy < grid_height and objects[i][x_min, move_gray_posy] == Color.GREY:
                    pos_y_min, pos_y_max = y_min + move, y_max + move
                    objects[i][x_min, move_gray_posy] = color
        
        # For each object except the last one, change the color of the right grey grid to the object's color
        if i < object_number - 1:
            gray_posy = [i for i, x in enumerate(objects[i][x_max]) if x == Color.GREY][0]
            objects[i][x_max, gray_posy] = color
            pre_right_gray_posy = gray_posy - y_min + pos_y_min
        
        # Copy the objects to output_grid
        blit(output_grid, objects[i][x_min : x_max + 1, y_min : y_max + 1], x = pos_x_min, y = pos_y_min)
        process_width = pos_x_max + 1

    return output_grid

def generate_input() -> np.ndarray:
    # Define the initial dimensions of the grid
    n, m = 3, 20  
    # Initialize the grid with zeros (black color)
    grid = np.zeros((n, m), dtype=int) 

    # Randomly choose the number of patterns to generate
    # Exclude gray color for pattern generation
    colors = Color.NOT_BLACK.copy()
    colors.remove(Color.GREY)  
    object_number = random.choice([3, 4])

    # Initial starting position for the pattern
    start_posx, start_posy = random.choice([0, 1, 2]), 0

    # Generate color objects
    for i in range(object_number):
        # Choose a random color for the object and initialize the position to be colored
        c = random.choice(colors)
        posx, posy = start_posx, start_posy
        maxx, minx = start_posx, start_posx
        
        # Randomly choose the number of the grid of the object
        grid_number = random.choice([3, 4])
        for j in range(grid_number):
            # Color the grid on (posx, posy) to grey or the real color
            grid[posx, posy] = Color.GREY if (i > 0 and j == 0) or (j == grid_number - 1 and i < object_number - 1) else c
            
            # Extend the object, either go to the next column, or move in the rows
            next_grid_directions = [[0, 1]]
            if j < grid_number - 1 and posx > 0 and grid[posx - 1, posy] == Color.BLACK:
                next_grid_directions.append([-1, 0])
            if j < grid_number - 1 and posx < n - 1 and grid[posx + 1, posy] == Color.BLACK:
                next_grid_directions.append([1, 0])
            
            # Choose a random direction to extend the pattern
            next_grid_direction = random.choice(next_grid_directions)  
            posx += next_grid_direction[0]
            posy += next_grid_direction[1]
            maxx = max(maxx, posx)
            minx = min(minx, posx)

        # For each object except the first object, randomly move the object up or down
        if i > 0:
            move = random.randint(-minx, n - maxx - 1)
            sprite = np.copy(grid[minx : maxx + 1, start_posy : posy])
            all_zero = np.zeros((n, posy - start_posy), dtype = int)
            blit(grid, all_zero, x = 0, y = start_posy)
            blit(grid, sprite, x = minx + move, y = start_posy)

        # Update the starting position for the next object
        start_posx, start_posy = posx, posy + 1
    
    input_grid = np.zeros((n, start_posy - 1), dtype=int)
    blit(input_grid, grid, x = 0, y = 0)
    return input_grid.T

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
