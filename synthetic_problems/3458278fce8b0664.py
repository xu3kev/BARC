import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, color mapping

# description:
# In the input you will see two separated bitmasks (one maroon and one teal) divided by a blue vertical bar.
# Each bitmask represents an image of specific objects. 
# To make the output map each object from the left bitmask to the right bitmask according to specific color mappings: 
# maroon -> grey, teal -> orange, keeping the output shape the same as the input.
# Finally, combine the results from the two separated bitmasks using logical AND operation.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the blue vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.BLUE):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]

    # Color mapping
    color_map = {
        Color.MAROON: Color.GREY,
        Color.TEAL: Color.ORANGE
    }

    mapped_left = np.vectorize(lambda color: color_map.get(color, color))(left_mask)
    mapped_right = np.vectorize(lambda color: color_map.get(color, color))(right_mask)

    # Perform logical AND on the mapped masks
    output_grid = np.zeros_like(left_mask)
    output_grid[(mapped_left == Color.GREY) & (mapped_right == Color.GREY)] = Color.GREY
    output_grid[(mapped_left == Color.ORANGE) & (mapped_right == Color.ORANGE)] = Color.ORANGE

    # Merge the result into a single grid with a blue separator
    final_grid = np.concatenate((mapped_left, np.full((1, left_mask.shape[1]), fill_value=Color.BLUE), output_grid), axis=0)
    
    return final_grid


def generate_input() -> np.ndarray:
    # create a pair of equally sized maroon and teal bitmasks
    width, height = np.random.randint(2, 10), np.random.randint(2, 10)

    left_grid = np.zeros((width, height), dtype=int)
    right_grid = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            if np.random.choice([True, False]):
                left_grid[x, y] = Color.MAROON  # maroon objects in the left bitmask
            if np.random.choice([True, False]):
                right_grid[x, y] = Color.TEAL    # teal objects in the right bitmask
    
    # create a blue vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.BLUE

    grid = np.concatenate((left_grid, bar, right_grid), axis=0)

    return grid