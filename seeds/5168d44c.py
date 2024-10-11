from common import *

import numpy as np
from typing import *

# concepts:
# collision, translation

# description:
# In the input you will see a red object overlaid on a track of green dots.
# To make the output, move the red object one green dot to the right (if the track is horizontal) or one green dot down (if the track is vertical).

def main(input_grid):
    # Plan:
    # 1. Detect the objects
    # 2. Determine the orientation of the track of green dots
    # 3. Move in the appropriate direction until it perfectly fits over the next green dot, meaning there are no collisions

    objects = find_connected_components(input_grid, connectivity=8, background=Color.BLACK, monochromatic=True)

    red_objects = [ obj for obj in objects if Color.RED in object_colors(obj, background=Color.BLACK) ]
    green_objects = [ obj for obj in objects if Color.GREEN in object_colors(obj, background=Color.BLACK) ]

    assert len(red_objects) == 1, "There should be exactly one red object"
    assert len(green_objects) >= 1, "There should be at least one green object"

    red_object = red_objects[0]

    # Determine the orientation of the track of green dots by comparing the positions of two dots
    x1,y1 = min( object_position(obj, anchor="center") for obj in green_objects )
    x2,y2 = max( object_position(obj, anchor="center") for obj in green_objects )
    if x1 == x2:
        # vertical track
        dx, dy = 0, 1
    elif y1 == y2:
        # horizontal track
        dx, dy = 1, 0
    
    # Make the output grid: Start with all the greens, then put the red in the right spot by moving it one-by-one
    output_grid = np.full_like(input_grid, Color.BLACK)
    for green_object in green_objects:
        blit_object(output_grid, green_object)

    for distance in range(1, 100):
        translated_red_object = translate(red_object, dx*distance, dy*distance)
        if not collision(object1=translated_red_object, object2=output_grid):
            blit_object(output_grid, translated_red_object)
            break

    return output_grid

def generate_input():
    # Make a grid with a red rectangle on the bottom and a teal diagonal line at the top pointing at it
    # Then randomly rotate to get a variety of orientations

    width, height = np.random.randint(10, 25), np.random.randint(10, 25)
    grid = np.full((width, height), Color.BLACK)

    # the red object will be a rectangle with a hole in the middle that the green dot fits into
    # for the hole to fit perfectly in the middle, it needs to be of odd dimension
    rectangle_width, rectangle_height = random.choice([3, 5]), random.choice([3, 5])
    red_rectangle = np.full((rectangle_width, rectangle_height), Color.RED)

    # randomly place the red rectangle at least 5 pixels away from the edge
    x, y = random_free_location_for_sprite(grid, red_rectangle, background=Color.BLACK, border_size=5)
    blit_sprite(grid, red_rectangle, x, y, background=Color.BLACK)

    # Create a row of green dots, starting with the center of the rectangle
    center_x, center_y = object_position(grid, anchor="center", background=Color.BLACK)
    grid[center_x, center_y] = Color.GREEN

    # create a horizontal row of green dots
    for i in range(-10, 10):
        dx = rectangle_width
        if 0 <= center_x + i*dx < width:
            grid[center_x + i*dx, center_y] = Color.GREEN
    
    # randomly flip/rotate
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
