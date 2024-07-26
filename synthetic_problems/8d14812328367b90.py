from common import *
import numpy as np
from typing import *

# concepts:
# symmetry, color, objects, rotation

# description:
# In the input, there is a symmetric object composed of random colors on a black background.
# The object will be horizontally or vertically symmetric.
# Additionally, there will be a colored rectangle in the top left corner of the grid indicating the rotation direction: red for 90 degrees clockwise and blue for 90 degrees counterclockwise.
# To make the output, rotate the symmetric object according to the direction indicated by the colored rectangle without altering the symmetry.

def main(input_grid: np.ndarray) -> np.ndarray:
    background_color = Color.BLACK

    # Check the color in the top-left corner to determine rotation direction
    direction_color = input_grid[0, 0]
    
    assert direction_color in [Color.RED, Color.BLUE], "Direction indicator must be either red or blue"

    # Exclude the direction indicator for object detection (crop it out)
    input_grid_cropped = input_grid[1:, 1:]

    # Find the object and crop it out
    objects = find_connected_components(input_grid_cropped, background=Color.BLACK, monochromatic=False)
    assert len(objects) == 1, "There should be exactly one object in the cropped area"
    object_grid = crop(objects[0], background=Color.BLACK)
    
    # Detect symmetry
    symmetries = detect_mirror_symmetry(object_grid, ignore_colors=[Color.BLACK])
    assert len(symmetries) == 1, "Object should have either horizontal or vertical symmetry"

    # Rotate the object
    if direction_color == Color.RED:  # 90 degrees clockwise
        rotated_object = np.rot90(object_grid, k=-1)
    elif direction_color == Color.BLUE:  # 90 degrees counterclockwise
        rotated_object = np.rot90(object_grid, k=1)

    # Place the rotated object back in the grid
    output_grid = np.copy(input_grid)
    output_grid[1:rotated_object.shape[0]+1, 1:rotated_object.shape[1]+1] = rotated_object

    return output_grid

def generate_input() -> np.ndarray:
    # Create a grid of random size between 10 and 15
    n = np.random.randint(10, 15)
    m = np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Determine the rotation direction and place the indicator in the top left corner (note except for Color.BLACK)
    direction_color = np.random.choice([Color.RED, Color.BLUE])
    grid[0, 0] = direction_color

    # Create a random symmetric object (horizontally or vertically)
    symmetry_type = np.random.choice(["horizontal", "vertical"])
    object_color = random.sample(list(Color.NOT_BLACK), 1)[0]

    sprite = random_sprite(np.random.randint(3, n-2), np.random.randint(3, m-2), density=0.5, symmetry=symmetry_type, color_palette=[object_color])

    # Find a random location in the grid to place the object, avoiding top-left corner
    free_location = False
    while not free_location:
        sprite_x, sprite_y = np.random.randint(1, n-sprite.shape[0]), np.random.randint(1, m-sprite.shape[1])
        if not collision(object1=grid, object2=sprite, x2=sprite_x, y2=sprite_y, background=Color.BLACK):
            free_location = True
    blit_sprite(grid, sprite, x=sprite_x, y=sprite_y)

    return grid