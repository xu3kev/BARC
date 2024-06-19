from common import *

import numpy as np
from typing import *


# concepts:
# patterns, growing, horizontal/vertical bars

# description:
# In the input you will see a 30x30 grid with at least two rectangles, each with at least one special pixel of a different color, and a crosshair-type pattern outside these rectangles.
# For each of these special pixels, apply the crosshair pattern and extend the points inside the rectangle that special pixel is in, until it reaches the edge.

def main(input_grid):
    # first get the grid size
    n, m = input_grid.shape

    # figure out background color
    background_color = input_grid[0][0]

    # with this background color, find the polychromatic objects, ### NOTE: 4-way connectivity works with input examples, 8-way may be more robust against other examples though
    objects = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=False)

    # sort the objects by their size in terms of area, the crosshair is the smallest object
    sorted_objects = sorted(objects, key=lambda x: np.count_nonzero(x))
    crosshair_object = sorted_objects[0]
    rectangles = sorted_objects[1:]

    # now find the crosshair sprite coordinates
    crosshair_sprite = crop(crosshair_object)
    width, height = crosshair_sprite.shape
    
    # if the crosshair is wider than it is tall, it extends horizontally, vertically if taller, both if square
    horizontal = True
    vertical = True
    if width > height:
        vertical = False
        point_color = crosshair_sprite[0, height // 2]
    elif height > width:
        horizontal = False
        point_color = crosshair_sprite[width // 2, 0]
    else:
        point_color = crosshair_sprite[width // 2, 0]

    # now we prepare the output grid
    output_grid = np.full_like(input_grid, background_color)

    # for each rectangle, crop it to just the rectangle, find the special pixel, extend the crosshair pattern from it, then add it back to the grid
    for rectangle in rectangles:
        # find the special color, it is the least common color in the rectangle
        colors, counts = np.unique(rectangle, return_counts=True)
        # colors are sorted by their frequency, so choose least common as the special color
        special_color = colors[-1]
        rectangle_color = colors[-2]

        # crop the rectangle to just the rectangle, while preserving its position in the grid
        rec_x, rec_y, w, h = bounding_box(rectangle)
        cropped_rectangle = crop(rectangle)
        
        # for each special pixel, extend the crosshair pattern
        for x, y in np.argwhere(cropped_rectangle == special_color):
            # first color the special pixel with the crosshair sprite centered on it
            cropped_rectangle = blit(cropped_rectangle, crosshair_sprite, x - width // 2, y - height // 2, background=Color.BLACK)

            # then extend the points in the crosshair pattern until they reach the edge of the rectangle
            if horizontal:
                for x0 in range(w):
                    if cropped_rectangle[x0, y] == rectangle_color:
                        cropped_rectangle[x0, y] = point_color
            if vertical:
                for y0 in range(h):
                    if cropped_rectangle[x, y0] == rectangle_color:
                        cropped_rectangle[x, y0] = point_color
        
        # add the rectangle back to the grid
        blit(output_grid, cropped_rectangle, rec_x, rec_y)

    return output_grid


def generate_input():
    # first set the grid dimensions, a random background color, and create the grid
    background_color = np.random.choice(Color.NOT_BLACK)
    n, m = 30, 30
    grid = np.full((n, m), background_color)

    # choose a random special color that is not the same as the background color
    special_color = new_random_color([background_color])

    # choose a random point color that is not already used
    point_color = new_random_color([background_color, special_color])

    # randomly choose rectangle color
    rectangle_color = new_random_color([background_color, special_color, point_color])

    # randomly choose if the crosshair uses an additional color
    additional_color_used = random.choice([True, False])
    if additional_color_used:
        additional_color = new_random_color([background_color, special_color, point_color, rectangle_color])

    # randomly choose the crosshair pattern
    crosshair_pattern = random.choice(['combined', 'horizontal', 'vertical'])

    # crosshair pattern size is dependent on the pattern, but is always 5x5, 3x5, or 5x3
    if crosshair_pattern == 'combined':
        # create the pattern and color the center pixel with the special color
        crosshair_sprite = np.zeros((5, 5), dtype=int)
        crosshair_sprite[:, 2] = point_color
        crosshair_sprite[2, :] = point_color
        crosshair_sprite[2, 2] = special_color

        # if an additional color is used, color the corners with it
        if additional_color_used:
            crosshair_sprite[1, 1] = additional_color
            crosshair_sprite[1, 3] = additional_color
            crosshair_sprite[3, 1] = additional_color
            crosshair_sprite[3, 3] = additional_color
    elif crosshair_pattern == 'horizontal':
        # create the pattern and color the center pixel with the special color
        crosshair_sprite = np.zeros((5, 3), dtype=int)
        crosshair_sprite[:, 1] = point_color
        crosshair_sprite[2, 1] = special_color

        # if an additional color is used, color the top and bottom with it
        if additional_color_used:
            extra_color = additional_color
        else:
            extra_color = special_color
        crosshair_sprite[1:4, 0] = extra_color
        crosshair_sprite[1:4, 2] = extra_color
    else:
        # create the pattern and color the center pixel with the special color
        crosshair_sprite = np.zeros((3, 5), dtype=int)
        crosshair_sprite[1, :] = point_color
        crosshair_sprite[1, 2] = special_color

        # if an additional color is used, color the top and bottom with it
        if additional_color_used:
            extra_color = additional_color
        else:
            extra_color = special_color
        crosshair_sprite[0, 1:4] = extra_color
        crosshair_sprite[2, 1:4] = extra_color

    # create a helper function to create the rectangles
    def create_rectangle(width, height):
        print("creating rectangle", width, height)
        # create empty rectangle
        to_return = np.full((width, height), rectangle_color)

        # randomly choose number of special pixels
        num_special = random.randint(1, 2)

        # create a list to store the special pixel locations
        special_pixels = []

        # create a list of possible special pixel locations
        possible_specials = [(x, y) for x in range(1, width - 1) for y in range(1, height - 1)]

        # randomly choose the location of the special pixels
        for _ in range(num_special):
            # randomly choose the location of the special pixel
            x, y = random.choice(possible_specials)
            
            # add the special pixel to the list of special pixels
            special_pixels.append((x, y))

            # remove valid locations around the special pixel
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (x + i, y + j) in possible_specials:
                        possible_specials.remove((x + i, y + j))

            # if there are no more valid locations, break
            if not possible_specials:
                break
        
        # place the special pixels onto the rectangle
        for x, y in special_pixels:
            to_return[x, y] = special_color

        return to_return

    # create a variable to track if the generated input was able to complete successfully
    clean_generation = False
    
    # loop over grid generation until a clean generation is achieved
    count = 0
    while not clean_generation:
        print("looping{}", count)
        count += 1
        # set clean generation to True
        clean_generation = True

        # randomly choose the number of rectangles (2 or 3)
        num_rectangles = random.randint(2, 3)

        # randomly choose the width and height of the first rectangle
        min_size = 7
        max_size = 16
        first_rec_size = [random.randint(min_size, max_size) for _ in range(2)]

        # create the first rectangle
        first_rectangle = create_rectangle(*first_rec_size)

        # first rectangle should be by one of the corners, with either 1 or 2 empty pixels on each edge
        x_options = [1, 2, n - first_rec_size[0] - 2, n - first_rec_size[0] - 3]
        y_options = [1, 2, m - first_rec_size[1] - 2, m - first_rec_size[1] - 3]

        # randomly choose the location of the first rectangle
        first_rec_x = random.choice(x_options)
        first_rec_y = random.choice(y_options)

        # place the first rectangle onto the grid
        blit(grid, first_rectangle, first_rec_x, first_rec_y)

        # for each additional rectangle, choose a random size and find a location to place it, ensuring it does not contact any other rectangle
        for _ in range(num_rectangles - 1):
            # randomly choose the width and height of the rectangle
            rec_size = [random.randint(min_size, max_size) for _ in range(2)]

            # create the rectangle
            rectangle = create_rectangle(*rec_size)

            # try to find a location to place the rectangle
            try :
                rec_x, rec_y = random_free_location_for_object(grid, rectangle, background_color=background_color, padding=1)
                blit(grid, rectangle, rec_x, rec_y)
            except:
                print("failed to place rectangle")
                # if the rectangle cannot be placed, the generation is not clean
                clean_generation = False
                break
        
        # now that all rectangles are placed, check if the crosshair pattern can be placed
        try:
            # find a location to place the crosshair pattern
            cross_x, cross_y = random_free_location_for_object(grid, crosshair_sprite, background_color=background_color)

            # place the crosshair pattern onto the grid
            blit(grid, crosshair_sprite, cross_x, cross_y)
        except:
            print("failed to place crosshair")
            # if the crosshair pattern cannot be placed, the generation is not clean
            clean_generation = False

        # if the generation was not clean, clear the grid and try again
        if not clean_generation:
            grid.fill(background_color)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)