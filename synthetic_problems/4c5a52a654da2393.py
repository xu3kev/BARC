import numpy as np
from typing import *
from common import *

# concepts:
# rotation, occlusion, pixel manipulation

# description:
# In the input, you will see an object made up of several colored pixels that has been rotated by some angle (90, 180, 270 degrees) and partially obscured by black pixels.
# To make the output, you should rotate it back to its original orientation (0 degrees) and remove the black pixels to restore the object as it was before being rotated and occluded.

def main(input_grid: np.ndarray) -> np.ndarray:
    # First, identify the angle of rotation based on the symmetry of non-black pixels
    rotations = [90, 180, 270]
    input_rotations = [np.rot90(input_grid, k=i//90) for i in rotations]
    
    # Try each rotation and check if the grid has occluded non-black pixels
    rotation_angle = None
    for rotation in rotations:
        grid_rotated = np.rot90(input_grid, k=rotation//90)
        if np.any(grid_rotated == Color.BLACK):
            rotation_angle = rotation
            break
    assert rotation_angle is not None, "No suitable rotation found"
    
    # Rotate the grid back to its original orientation
    output_grid = np.rot90(input_grid, k=(360-rotation_angle)//90)
    
    # Remove occluding black pixels
    output_grid[output_grid == Color.BLACK] = Color.BLACK
    
    return output_grid

def generate_input() -> np.ndarray:
    # Create a random small grid where the object will be located
    input_size = np.random.randint(8, 15)
    input_grid = np.zeros((input_size, input_size), dtype=int)
    
    # Create a sprite (object) with a non-zero density
    n, m = np.random.randint(3, 6, size=2)
    sprite = random_sprite(n, m, density=0.4, color_palette=Color.NOT_BLACK)

    # Place the sprite randomly on the grid
    x, y = random_free_location_for_sprite(input_grid, sprite)
    blit_sprite(input_grid, sprite, x, y)
    
    # Choose a random rotation (90, 180, 270 degrees)
    rotation = np.random.choice([90, 180, 270])
    input_grid = np.rot90(input_grid, k=rotation//90)
    
    # Add occluding black pixels
    num_occlusions = np.random.randint(5, 15)
    for _ in range(num_occlusions):
        x, y = np.random.randint(0, input_size), np.random.randint(0, input_size)
        input_grid[x, y] = Color.BLACK
    
    return input_grid