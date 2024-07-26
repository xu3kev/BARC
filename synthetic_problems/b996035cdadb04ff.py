from common import *

import numpy as np
from typing import *

# concepts:
# patterns, objects, alignment by color, horizontal/vertical bars

# description:
# In the input, you will see rectangular objects scattered around. Each object has a vertical bar and a horizontal bar of a unique color intersecting at a special blue pixel.
# To make the output, align all objects by their special blue pixels vertically and extend their vertical bars until they intersect with another object's bar or the edge of the grid.

def main(input_grid):
    # Find all objects in the grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # Find the background color
    background_color = np.bincount(input_grid.flatten()).argmax()
    
    # Create an output grid
    output_grid = np.full(input_grid.shape, background_color)
    
    # List to store the x-coordinates (row) of all the special blue pixels
    blue_positions = []
    
    # Extract each object's sprite, identify the special blue pixel, and append the x-coordinate to blue_positions
    sprites = []
    for obj in objects:
        sprite = crop(obj, background=background_color)
        sprites.append(sprite)
        blue_y, blue_x = np.argwhere(sprite == Color.BLUE)[0]
        blue_positions.append(blue_x)
    
    # Sort blue_positions to align objects vertically
    blue_positions.sort()
    
    # Align each object vertically
    for i, sprite in enumerate(sprites):
        blue_y, blue_x = np.argwhere(sprite == Color.BLUE)[0]
        
        # Move blue pixel to the i-th position in the sorted list
        target_x = blue_positions[i]
        
        # Calculate the top left corner of where to place this sprite in the output grid
        top_left_y = blue_y
        top_left_x = target_x - blue_x
        
        # Place sprite in the output grid
        blit_sprite(output_grid, sprite, top_left_y, top_left_x, background=background_color)
    
    # Extend the vertical bars
    for x in blue_positions:
        # Extract the vertical line of pixels at column x
        column = output_grid[:, x]
        
        for y in range(len(column)):
            if column[y] != background_color:
                color = column[y]
                if color != Color.BLUE:
                    draw_line(output_grid, y, x, length=None, color=color, direction=(1, 0))
                    draw_line(output_grid, y, x, length=None, color=color, direction=(-1, 0))
                    break
    
    return output_grid


def generate_input():
    # Define grid size
    grid_size = np.random.randint(12, 17)
    
    # Create an empty grid
    grid = np.full((grid_size, grid_size), Color.BLACK)

    # Decide how many objects to generate
    num_objects = np.random.randint(2, 5)

    # For each object, generate a vertical and horizontal bar that intersect at a blue pixel
    for _ in range(num_objects):
        sprite_size = np.random.randint(3, 5)
        
        # Create a new sprite
        sprite = np.full((sprite_size, sprite_size), Color.BLACK)
        
        # Choose a random color for the bars
        bar_color = np.random.choice(list(Color.NOT_BLACK))
        
        # Add vertical and horizontal bars
        center = sprite_size // 2
        sprite[:, center] = bar_color
        sprite[center, :] = bar_color
        
        # Add the special blue pixel where the bars intersect
        sprite[center, center] = Color.BLUE
        
        # Place the sprite randomly in the grid but ensuring they do not overlap
        top_left_y, top_left_x = random_free_location_for_sprite(grid, sprite, padding=2, border_size=2)
        blit_sprite(grid, sprite, top_left_y, top_left_x, background=Color.BLACK)

    return grid