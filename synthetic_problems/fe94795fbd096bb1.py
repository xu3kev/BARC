from common import *
import numpy as np
from typing import *

# concepts:
# collision detection, sliding objects, translational symmetry

# description:
# In the input you will see a grid with a blue L-shaped object and a green T-shaped object.
# The blue L-shaped object needs to slide horizontally until it just touches the green T-shaped
# object while maintaining its translational symmetry (mirror-symmetric about the
# starting column). 

def main(input_grid):
    n, m = input_grid.shape

    # Extract the blue L-shaped object
    blue_l_object = np.zeros_like(input_grid)
    blue_l_object[input_grid == Color.BLUE] = Color.BLUE

    # Extract the green T-shaped object
    green_t_object = np.zeros_like(input_grid)
    green_t_object[input_grid == Color.GREEN] = Color.GREEN

    # The output grid starts with the initial position of the T-shaped object
    output_grid = np.copy(green_t_object)

    # Get the initial position of the L-shaped object
    initial_x, initial_y = np.argwhere(blue_l_object)[0]

    # Consider sliding to the right while maintaining the translational symmetry
    for slide_distance in range(1, m - initial_y):
        translated_blue_l = translate(blue_l_object, 0, slide_distance, background=Color.BLACK)
        if contact(object1=translated_blue_l, object2=green_t_object, background=Color.BLACK):
            blit_object(output_grid, translated_blue_l, background=Color.BLACK)
            break

    return output_grid

# Function to generate random L-shaped object
def generate_l_shape():
    l_shape = np.array([
        [1, 0],
        [1, 0],
        [1, 1]
    ], dtype=int)
    return l_shape

# Function to generate random T-shaped object
def generate_t_shape():
    t_shape = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ], dtype=int)
    return t_shape

def generate_input():
    # Create a random grid of size between 5x5 and 10x10
    n, m = np.random.randint(5, 11), np.random.randint(5, 11)
    grid = np.full((n, m), Color.BLACK)

    # Insert the L-shaped object on the left half of the grid
    l_shape = generate_l_shape()
    l_x, l_y = np.random.randint(0, n - l_shape.shape[0]), np.random.randint(0, m // 2 - l_shape.shape[1])
    grid[l_x:l_x + l_shape.shape[0], l_y:l_y + l_shape.shape[1]][l_shape == 1] = Color.BLUE

    # Insert the T-shaped object on the right half of the grid
    t_shape = generate_t_shape()
    t_x, t_y = np.random.randint(0, n - t_shape.shape[0]), np.random.randint(m // 2, m - t_shape.shape[1])
    grid[t_x:t_x + t_shape.shape[0], t_y:t_y + t_shape.shape[1]][t_shape == 1] = Color.GREEN

    # Ensure there could be a possible slide horizontally.

    return grid