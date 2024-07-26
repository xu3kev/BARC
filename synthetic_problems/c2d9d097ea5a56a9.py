from common import *
import numpy as np

# concepts:
# color, patterns, cropping

# description:
# In the input, you will see a grid with several random patterns of different colors. 
# The output should identify the largest pattern on the input grid, change all its colors to blue, 
# and crop out the largest pattern with a single-pixel black border around it.

def main(input_grid):
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=False)
    max_object = max(objects, key=lambda obj: np.sum(obj != Color.BLACK))
    output_grid = input_grid.copy()
    
    # Color the largest object blue
    max_object[max_object != Color.BLACK] = Color.BLUE
    blit_object(output_grid, max_object, background=Color.BLACK)
    
    # Crop the largest object
    cropped_object = crop(output_grid, background=Color.BLACK)
    
    # Create the final output grid with a black border around the cropped object
    final_output_size = (cropped_object.shape[0] + 2, cropped_object.shape[1] + 2)
    final_output_grid = np.full(final_output_size, Color.BLACK, dtype=output_grid.dtype)
    final_output_grid[1:-1, 1:-1] = cropped_object
    
    return final_output_grid

def generate_input():
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    input_grid = np.full((n, m), Color.BLACK, dtype=int)
    
    # Add random patterns
    num_patterns = np.random.randint(3, 6)
    for _ in range(num_patterns):
        pattern = random_sprite(np.random.randint(3, 6), np.random.randint(3, 6), color_palette=Color.NOT_BLACK)
        try:
            x, y = random_free_location_for_sprite(input_grid, pattern, padding=1)
            blit_sprite(input_grid, pattern, x=x, y=y)
        except ValueError:
            continue
    
    return input_grid

# Example usage: