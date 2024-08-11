import numpy as np
from typing import *
from common import *

# concepts:
# symmetry detection, occlusion, pixel manipulation

# description:
# In the input, you will see a grid with an object that is vertically symmetric but partially occluded by black pixels randomly placed.
# The task is to restore vertical symmetry by filling in missing pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find vertical symmetry
    sym = detect_translational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    
    # Calculate the width and height of the grid
    height, width = input_grid.shape
    
    # Initialize the output grid as a copy of the input
    output_grid = input_grid.copy()

    # Ensure the grid has vertical symmetry by copying columns symmetrically replacing occluded parts
    for x in range(width // 2):
        for y in range(height):
            if output_grid[y, x] == Color.BLACK and input_grid[y, width - x - 1] != Color.BLACK:
                output_grid[y, x] = input_grid[y, width - x - 1]
            if output_grid[y, width - x - 1] == Color.BLACK and input_grid[y, x] != Color.BLACK:
                output_grid[y, width - x - 1] = input_grid[y, x]
            
    return output_grid

def generate_input() -> np.ndarray:
    height = np.random.randint(10, 15)
    width = np.random.randint(10, 15)
    
    # Create an empty grid
    grid = np.full((height, width), Color.BLACK)

    # Create a sprite with vertical symmetry
    sprite_height = np.random.randint(3, height // 2)
    sprite_width = np.random.randint(3, width // 2)
    sprite = np.zeros((sprite_height, sprite_width), dtype=int)
    color_palette = list(Color.NOT_BLACK)
    
    # Fill the left half of the sprite with colors
    for i in range(sprite_height):
        for j in range(sprite_width // 2):
            sprite[i, j] = np.random.choice(color_palette)
            
    # Mirror the left half to the right half
    sprite[:, sprite_width // 2:] = sprite[:, :sprite_width // 2][:, ::-1]

    # Place the sprite randomly on the grid
    x, y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x, y)

    # Add random occlusions
    num_occlusions = np.random.randint(5, 10)
    for _ in range(num_occlusions):
        ox = np.random.randint(width)
        oy = np.random.randint(height)
        grid[oy, ox] = Color.BLACK
    
    return grid