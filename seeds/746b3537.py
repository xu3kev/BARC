from common import *

import numpy as np
from typing import *

# concepts:
# line detection, color extraction

# description:
# In the input you will see a grid consisting of stripes that are either horizontal or vertical.
# To make the output, make a grid with one pixel for each stripe whose color is the same color as that stripe.
# If the stripes are vertical, the output should be vertical, and if the stripes are horizontal, the output should be horizontal. The colors should be in the order they appear in the input.

def main(input_grid):
    # Parse input and then determine the orientation of the stripes
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True, background=Color.BLACK)
    x_positions = [ object_position(obj, background=Color.BLACK, anchor="center")[0] for obj in objects]
    y_positions = [ object_position(obj, background=Color.BLACK, anchor="center")[1] for obj in objects]
    if all(x == x_positions[0] for x in x_positions):
        orientation = "vertical"
    elif all(y == y_positions[0] for y in y_positions):
        orientation = "horizontal"
    else:
        raise ValueError("The stripes are not aligned in a single axis")
    
    # Sort the objects depending on the orientation
    if orientation == "horizontal":
        objects.sort(key=lambda obj: object_position(obj, background=Color.BLACK, anchor="center")[0])
    else:
        objects.sort(key=lambda obj: object_position(obj, background=Color.BLACK, anchor="center")[1])
    
    # Extract the colors of the stripes
    colors = [ object_colors(obj, background=Color.BLACK)[0] for obj in objects ]

    # Generate the output grid
    if orientation == "horizontal":
        output_grid = np.full((len(colors), 1), Color.BLACK)
        output_grid[:, 0] = colors
    else:
        output_grid = np.full((1, len(colors)), Color.BLACK)
        output_grid[0, :] = colors
    
    return output_grid
    


def generate_input():
    # Generate grid of size n x m
    n, m = np.random.randint(3, 10), np.random.randint(2, 10)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose n colors
    colors = np.random.choice(list(Color.NOT_BLACK), n)
    
    # Draw vertical lines of the chosen colors
    for x, color in enumerate(colors):
        draw_line(grid, x=x, y=0, length=m, color=color, direction=(0, 1))
        # same as grid[x,:] = color
    
    # Randomly rotate the whole grid to make the lines horizontal or vertical
    if random.random() < 0.5:
        grid = np.rot90(grid)

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
