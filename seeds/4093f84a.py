from common import *

import numpy as np
from typing import *

# concepts:
# attraction, magnetism, color change

# description:
# In the input you will see a grey rectangle and colored pixels scattered around it.
# To make the output, move each colored pixel toward the grey rectangle until it touches, then turn its color to gray. If multiple colored pixels collide, they stack.

def main(input_grid):
    # Plan:
    # 1. Detect the objects; separate the gray rectangle from the other pixels
    # 2. Move each colored pixel toward the gray rectangle until it touches
    # 3. Change its color once it touches

    objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK, monochromatic=True)

    grey_objects = [ obj for obj in objects if Color.GREY in object_colors(obj, background=Color.BLACK) ]
    other_objects = [ obj for obj in objects if Color.GREY not in object_colors(obj, background=Color.BLACK) ]

    assert len(grey_objects) == 1, "There should be exactly one grey object"
    
    grey_object = grey_objects[0]

    # Make the output grid: Start with the gray object, then add the colored pixels one-by-one
    output_grid = np.full_like(input_grid, Color.BLACK)
    blit_object(output_grid, grey_object)

    # Move the colored objects and change their color once they hit grey
    for colored_object in other_objects:
        # First calculate what direction we have to move in order to contact the grey object
        # Consider all displacements, starting with the smallest translations first
        possible_displacements = [ (i*dx, i*dy) for i in range(0, 30) for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)] ]

        # Only keep the displacements that cause a contact between the colored object and the grey object
        valid_displacements = [ displacement for displacement in possible_displacements
                                if contact(object1=translate(colored_object, *displacement), object2=grey_object) ]
        assert valid_displacements, "There should be at least one valid displacement"

        # Pick the smallest valid displacement
        displacement = min(valid_displacements, key=lambda displacement: sum(abs(x) for x in displacement))

        # Extract the direction from the displacement
        direction = np.sign(displacement, dtype=int)

        # Now move the colored object in that direction until there is a collision with something else
        if not all( delta == 0 for delta in direction ):
            while not collision(object1=translate(colored_object, *direction), object2=output_grid):
                colored_object = translate(colored_object, *direction)
        
        # Finally change the color of the colored object to grey anne draw it onto the outlet
        colored_object[colored_object != Color.BLACK] = Color.GREY
        blit_object(output_grid, colored_object)
    
    return output_grid

def generate_input():
    # Make a grid with a grey horizontal rectangle stretching all the way through the middle, and some scattered points around it
    # Then randomly rotate to get a variety of orientations

    width, height = np.random.randint(10, 25), np.random.randint(10, 25)
    grid = np.full((width, height), Color.BLACK)

    rectangle_y1 = np.random.randint(0, height//2)
    rectangle_y2 = np.random.randint(height//2, height)
    grid[:, rectangle_y1:rectangle_y2] = Color.GREY

    # scatter some colored pixels around the grey rectangle
    for _ in range(np.random.randint(5, 10)):
        random_color = random.choice([color for color in Color.NOT_BLACK if color != Color.GREY])
        pixel_sprite = np.full((1,1), random_color)
        x, y = random_free_location_for_sprite(grid, pixel_sprite, background=Color.BLACK)
        blit_sprite(grid, pixel_sprite, x, y, background=Color.BLACK)
    
    # random rotation
    grid = np.rot90(grid, np.random.randint(0, 4))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
