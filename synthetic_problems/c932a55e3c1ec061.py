from common import *

import numpy as np
from typing import *

# concepts:
# rotational patterns, colors

# description:
# In the input, you will see a grid with colored pixels representing a pattern.
# The task is to rotate the entire grid by 90 degrees clockwise and produce the output.

def main(input_grid):
    # Rotate the grid by 90 degrees clockwise
    output_grid = np.rot90(input_grid, k=-1)  # k=-1 for clockwise rotation
    return output_grid

def generate_input():
    # Create a grid with random dimensions (between 5 and 10)
    width = np.random.randint(5, 11)
    height = np.random.randint(5, 11)
    
    # Fill the grid with random colors from the color palette
    input_grid = np.random.choice(list(Color.NOT_BLACK), size=(width, height))
    
    return input_grid