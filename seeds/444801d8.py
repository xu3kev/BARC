from common import *

import numpy as np
from typing import *

# concepts:
# cups, filling

# description:
# In the input you will see several blue "cups", meaning an almost-enclosed shape with a small opening at the top, and empty space (black pixels) inside, as well as a single colored pixel inside.
# To make the output grid, you should fill the interior of each cup with the same color as the colored pixel inside it. 
# Also, put a single layer of colored pixels above the cup with the same color as what's inside.

def main(input_grid):
    # Plan:
    # 1. Detect all the blue cups
    # 2. For each cup, find the mask of what is inside of it
    # 3. Find the color of the single pixel inside the cup
    # 4. Fill the cup with the color
    # 5. Put a single layer of colored pixels above the cup with the same color as what's inside
    
    # Detect all the blue cups
    blue_cups = detect_objects(grid=input_grid, colors=[Color.BLUE], monochromatic=True, connectivity=4)

    output_grid = input_grid.copy()

    # For each cup object...
    for obj in blue_cups:
        # Extract what's inside the cup (as its own object), which is everything in the bounding box that is not the object itself
        cup_x, cup_y, cup_width, cup_height = bounding_box(obj)
        inside_cup_mask = np.zeros_like(input_grid, dtype=bool)
        inside_cup_mask[cup_x:cup_x+cup_width, cup_y:cup_y+cup_height] = True
        inside_cup_mask = inside_cup_mask & (obj != Color.BLUE)
        object_inside_cup = np.where(inside_cup_mask, input_grid, Color.BLACK)        

        # Find the color of the single pixel inside the cup
        colors = object_colors(object_inside_cup, background=Color.BLACK)
        assert len(colors) == 1, "There should be exactly one color inside the cup"
        color = colors[0]

        # Fill the cup with the color
        output_grid[inside_cup_mask] = color

        # Put a single layer of colored pixels above the cup with the same color as what's inside
        top_y = cup_y - 1
        output_grid[cup_x:cup_x+cup_width, top_y] = color

    return output_grid

def generate_input():
    # Generate the grid with random size
    width = np.random.randint(8, 30)
    height = np.random.randint(8, 30)
    grid = np.full((width, height), Color.BLACK)

    n_cups = np.random.randint(1, 2+1)

    for cup_index in range(n_cups):
        # Pick a random width/height for this cup
        cup_width = np.random.randint(4, 8)
        cup_height = np.random.randint(3, 8)

        # Make a sprite, which is just going to be a blue outline of a rectangle with a hole at the top
        sprite = np.full((cup_width, cup_height), Color.BLACK)
        sprite[0, :] = Color.BLUE
        sprite[-1, :] = Color.BLUE
        sprite[:, 0] = Color.BLUE
        sprite[:, -1] = Color.BLUE

        # Make the hole centered at the top (variable size)
        hole_left_x = np.random.randint(1, cup_width//2)
        hole_right_x = cup_width - hole_left_x - 1
        hole_y = 0
        sprite[hole_left_x:hole_right_x+1, hole_y] = Color.BLACK

        # Put another color inside the cup
        color = np.random.choice([color for color in Color.NOT_BLACK if color != Color.BLUE])
        x, y = np.random.randint(1, cup_width-1), np.random.randint(1, cup_height-1)
        sprite[x, y] = color

        # Find a random free location for it
        free_x, free_y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, padding=1, border_size=1)
        blit_sprite(grid, sprite, free_x, free_y, background=Color.BLACK)

    return grid    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
