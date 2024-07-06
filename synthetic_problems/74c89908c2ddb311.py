from common import *
import numpy as np
from typing import *

# concepts:
# counting, objects, rotation, color transformation

# description:
# In the input you will see the grid containing colored objects on a black background.
# For each object, rotate its pixels 90 degrees clockwise if it has an even number of pixels, or counterclockwise if it has an odd number of pixels.
# The output grid shows the modified objects.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # Find connected components (objects) in the grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)
    
    for obj in objects:
        # Count the number of non-black pixels in the object
        pixel_count = np.sum(obj != Color.BLACK)
        
        # Determine the direction of rotation based on the pixel count
        if pixel_count % 2 == 0:
            # Rotate clockwise (90 degrees)
            rotated_obj = np.rot90(obj, k=-1)
        else:
            # Rotate counterclockwise (90 degrees)
            rotated_obj = np.rot90(obj, k=1)
        
        # Get bounding box of the object in the grid
        x, y, w, h = bounding_box(obj, background=Color.BLACK)
        
        # Clear the original object's area in the output grid
        output_grid[x:x+w, y:y+h] = Color.BLACK
        
        # Blit the rotated object back to the output grid
        blit(output_grid, rotated_obj, x, y, background=Color.BLACK)
    
    return output_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Create a random number of colorful objects and place them on the grid
    num_objects = np.random.randint(3, 10)
    for _ in range(num_objects):
        # Create a random object with random colors
        obj_height, obj_width = np.random.randint(2, n // 2), np.random.randint(2, m // 2)
        colors = [np.random.choice(list(Color.NOT_BLACK), size=(obj_height, obj_width), replace=True)]
        
        obj = np.zeros((obj_height, obj_width))
        for color in colors:
            obj = np.where(obj == 0, color, obj)
        
        # Place the object on the grid at a random free location
        try:
            x, y = random_free_location_for_object(grid, obj, padding=1, padding_connectivity=8)
            blit(grid, obj, x, y)
        except:
            pass  # Ignore if no space is available

    return grid