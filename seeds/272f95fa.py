from common import *

import numpy as np
from typing import *


# concepts:
# filling, intersection, horizontal/vertical bars

# description:
# In the input you will see a grid with two horizontal and two vertical teal bars with a black background.
# For each partitioned section in the grid, fill in the top, left, bottom, right, and middle sections with red, yellow, blue, green, and pink, respectively. Ignore the corner sections.

def main(input_grid):
    # first get the grid size
    n, m = input_grid.shape

    # before we can find the partitions, we need to recolor them to not be black, such as grey, so we can find the connected components
    input_grid[input_grid == Color.BLACK] = Color.GREY

    # find the connected components in the grid with teal as the background color, giving us the partitions
    partitions = find_connected_components(input_grid, background=Color.TEAL, connectivity=4, monochromatic=True)
    
    # for each partition, if it is one of the top, left, bottom, right, or middle sections, fill it with the appropriate color, otherwise recolor it to black
    for partition in partitions:
        # get the bounding box of the partition and set the max x and y values
        min_x, min_y, width, height = bounding_box(partition)
        max_x = min_x + width - 1
        max_y = min_y + height - 1

        # if the partition is in the top row and not touching either edge of the grid, fill that section with red
        if min_y == 0 and min_x > 0 and max_x < n - 1:
            flood_fill(input_grid, min_x, min_y, Color.RED)
        # else, if the partition is on the bottom row and not touching either edge of the grid, fill that section with blue
        elif max_y == m - 1 and min_x > 0 and max_x < n - 1:
            flood_fill(input_grid, min_x, min_y, Color.BLUE)
        # else, if it is in the middle row, then we need to check if it is touching the left, right, or neither edge of the grid
        elif min_y > 0 and max_y < m - 1:
            # if the partition is touching the left edge of the grid, fill it with yellow
            if min_x == 0:
                flood_fill(input_grid, min_x, min_y, Color.YELLOW)
            # else, if the partition is touching the right edge of the grid, fill it with green
            elif max_x == n - 1:
                flood_fill(input_grid, min_x, min_y, Color.GREEN)
            # otherwise, fill the partition with pink
            else:
                flood_fill(input_grid, min_x, min_y, Color.PINK)
        # else, the partition is not one of the sections we need to fill, so recolor it to black
        else:
            flood_fill(input_grid, min_x, min_y, Color.BLACK)
        
    return input_grid


def generate_input():
    # first set the grid dimensions, a random background color, and create the grid
    background_color = np.random.choice(Color.NOT_BLACK)
    n, m = 30, 30
    grid = np.full((n, m), background_color)

    # choose a random special color that is not the same as the background color
    special_color = new_random_color(not_allowed_colors=[background_color])

    # choose a random point color that is not already used
    point_color = new_random_color(not_allowed_colors=[background_color, special_color])

    # randomly choose rectangle color
    rectangle_color = new_random_color(not_allowed_colors=[background_color, special_color, point_color])

    # randomly choose if the crosshair uses an additional color
    additional_color_used = random.choice([True, False])
    if additional_color_used:
        additional_color = new_random_color(not_allowed_colors=[background_color, special_color, point_color, rectangle_color])

    # randomly choose the crosshair pattern
    crosshair_pattern = random.choice(['combined', 'horizontal', 'vertical'])

    # crosshair pattern size is dependent on the pattern, but is always 5x5, 3x5, or 5x3
    if crosshair_pattern == 'combined':
        # create the pattern and color the center pixel with the special color
        crosshair_sprite = np.full((5, 5), dtype=int, fill_value=background_color)
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
        crosshair_sprite = np.full((5, 3), dtype=int, fill_value=background_color)
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
        crosshair_sprite = np.full((3, 5), dtype=int, fill_value=background_color)
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
            for i in range(-2, 3):
                for j in range(-2, 3):
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
    while not clean_generation:
        # set clean generation to True
        clean_generation = True

        # randomly choose the number of rectangles (2 or 3)
        num_rectangles = random.randint(2, 3)

        # randomly choose the width and height of the first rectangle
        min_size = 7
        max_size = 18
        first_rec_size = [random.randint(min_size, max_size) for _ in range(2)]

        # create the first rectangle
        first_rectangle = create_rectangle(*first_rec_size)

        # first rectangle should be by one of the corners, with either 1 or 2 empty pixels on each edge
        x_options = [1, 2, n - first_rec_size[0] - 1, n - first_rec_size[0] - 2]
        y_options = [1, 2, m - first_rec_size[1] - 1, m - first_rec_size[1] - 2]

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
                rec_x, rec_y = random_free_location_for_object(grid, rectangle, background=background_color, border_size=1, padding=1)
                blit(grid, rectangle, rec_x, rec_y)
            except:
                # if at least two rectangles are placed, we can proceed with the crosshair pattern
                clean_generation = False
                break

        # if the generation was not clean to this point, clear the grid and try again
        if not clean_generation:
            grid.fill(background_color)
            continue
        
        # now that all rectangles are placed, check if the crosshair pattern can be placed
        try:
            # find a location to place the crosshair pattern
            cross_x, cross_y = random_free_location_for_object(grid, crosshair_sprite, background=background_color, border_size=1, padding=1)

            # place the crosshair pattern onto the grid
            blit(grid, crosshair_sprite, cross_x, cross_y)
        except:
            # if the crosshair pattern cannot be placed, the generation is not clean
            clean_generation = False

        # if the generation was not clean, clear the grid and try again
        if not clean_generation:
            grid.fill(background_color)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)