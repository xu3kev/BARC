from common import *

import numpy as np
from typing import *

# concepts:
# scaling, shape completion

# description:
# In the input you will see one pattern shape with one pixel of a different color as an indicator. 
# Several other shapes will be given, each with one pixel of a different color as an indicator and different scales.
# To make the output, scale the original shape to the same size and color as the other shapes by the size of indicator pixel.
# Place the scaled shape on the other shapes so that the indicator pixel is at the same position.

def main(input_grid):
    # The output grid transform from the input grid
    output_grid = input_grid.copy()

    # Extract all the objects from the input grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)

    # Find out the original shape and indicator shapes
    indicator_shapes = []
    color_list = []
    for object in objects:
        object_shape = crop(object)
        object_colors = np.unique(object_shape)
        color_count = [len(np.argwhere(object_shape == color)) for color in object_colors]

        # Collect all the colors' appearance in the objects to find the indicator pixel's color
        color_list.extend([color for color in object_colors if color != Color.BLACK])

        # The indicator shape only has two contact squares with different colors and same scale
        if len(color_count) == 2 and color_count[0] == color_count[1]:
            indicator_shapes.append(object)
        # Otherwise, it's the original shape
        else:
            original_shape = object_shape
    
    # The indicat pixel's color appear in all the indicator shapes and original shape
    indicate_color = color_list[np.argmax([np.sum(color_list == color) for color in color_list])]

    # Find out the relative position of the indicator pixel in the original shape
    indicate_position = np.argwhere(original_shape == indicate_color)

    # Find the original shape's color
    original_shape_color = [color for color in np.unique(original_shape) if color != Color.BLACK and color != indicate_color][0]

    for indicator_shape in indicator_shapes:
        # Find the new shape's color
        new_scale_shape_color =[color for color in np.unique(indicator_shape) if color != Color.BLACK and color != indicate_color][0]

        # Only leave the indicator pixel in the indicator shape
        indicator_shape[indicator_shape != indicate_color] = Color.BLACK

        # Get the indicator pixel's size and position
        x, y, w, h = bounding_box(indicator_shape)
        scale_factor = w

        # Scale the original pattern to the same scale
        original_shape_scale = scale_sprite(original_shape, scale_factor)

        # Change the original shape's color to the new shape's color
        original_shape_scale[original_shape_scale == original_shape_color] = new_scale_shape_color
        x_rela, y_rela = indicate_position[0]

        # Place the scaled original shape on the indicator shape, make sure the indicator pixel is at the same position
        x_grid, y_grid = x - x_rela * scale_factor, y - y_rela * scale_factor
        blit_sprite(output_grid, original_shape_scale, x=x_grid, y=y_grid)
        
    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(10, 25), np.random.randint(10, 25)
    grid = np.zeros((n, m), dtype=int)

    # Get the place holder to ensure the shapes after completition do not overlap
    place_holder = grid.copy()

    # Randomly select the color of objects and indicator pixel
    object_number = np.random.randint(2, 4)
    colors = np.random.choice(Color.NOT_BLACK, object_number + 1, replace=False)
    indicator_color, original_color = colors[0], colors[1]

    # Generate the original shape
    w, h = np.random.randint(3, 5), np.random.randint(3, 5)
    original_shape = random_sprite(n=w, m=h, color_palette=[original_color], connectivity=4)

    # Randomly turn one pixel into the indicator pixel
    indicator_pixel = random.choice(np.argwhere(original_shape == original_color))
    original_shape[indicator_pixel[0], indicator_pixel[1]] = indicator_color

    # Place the original shape on the grid
    x, y = random_free_location_for_sprite(grid=grid, sprite=original_shape)
    blit_sprite(grid=grid, sprite=original_shape, x=x, y=y)
    blit_sprite(grid=place_holder, sprite=original_shape, x=x, y=y)

    # Check which pixels are connected to the indicator pixel
    positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for pos in positions:
        x_contact, y_contact = indicator_pixel[0] + pos[0], indicator_pixel[1] + pos[1]
        if 0 <= x_contact < w and 0 <= y_contact < h and original_shape[x_contact, y_contact] == original_color:
            x1, x2 = min(indicator_pixel[0], x_contact), max(indicator_pixel[0], x_contact)
            y1, y2 = min(indicator_pixel[1], y_contact), max(indicator_pixel[1], y_contact)
            indicator_shape = original_shape.copy()[x1:x2+1, y1:y2+1]
            break
    
    # Place the indicator shape on the grid
    other_colors = colors[2:]
    for color in other_colors:
        # Change the object color
        cur_object = indicator_shape.copy()
        cur_object[cur_object == original_color] = color
        
        # Rescale the indicator shape
        scale = np.random.randint(1, 4)
        cur_object = scale_sprite(cur_object, scale)
        scaled_original = scale_sprite(original_shape, scale)

        # Place the original scaled object on the place_holder
        try:
            x, y = random_free_location_for_sprite(grid=place_holder, sprite=scaled_original, padding=1, padding_connectivity=8)
        # If there is not enough space, generate a new input
        except:
            return generate_input()
        blit_sprite(grid=place_holder, sprite=scaled_original, x=x, y=y)

        # Get the relative position of the scaled indicator shape
        x_rela, y_rela = x + indicator_pixel[0] * scale, y + indicator_pixel[1] * scale
        # Place the scaled indicator shape on the grid
        blit_sprite(grid=grid, sprite=cur_object, x=x_rela, y=y_rela)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
