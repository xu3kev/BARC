from common import *

import numpy as np
from typing import *

# concepts:
# filling

# description:
# The input consists of a black grid containing a few hollow grey rectangles. Each rectangle has 1-3 grey horizontal or vertical lines emanating off of it (at most one per side), either travelling to the border or stopping at another rectangle.
# To create the output, fill in the hollow grey rectangles with yellow.

def main(input_grid):
    # extract objects using grey as background
    objects = find_connected_components(input_grid, background=Color.GREY, connectivity=4, monochromatic=True)

    # create an output grid to store the result
    output_grid = np.full(input_grid.shape, Color.GREY)

    # for each object, fill it in if it is a rectangle
    for obj in objects:
        # to check if the object is a rectangle, we can check if the cropped object is entirely black
        sprite = crop(obj, background=Color.GREY)
        is_rectangle = np.all(sprite == Color.BLACK)

        if is_rectangle:
            # we also need to make sure the rectangle isn't caused from an emanating line.
            # to do so, make sure any grey pixels within 1 pixel of the grey border are not "extremal", aka dont have an x or y value equal to the grey pixel border's x/y value.
            x, y, w, h = bounding_box(obj, background=Color.GREY)
            # add a 1 pixel border for the grey border that's already there
            x -= 1
            y -= 1
            w += 2
            h += 2
            pixels_to_check = []
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                bordering_pixels = find_bordering_pixels_in_direction(x, y, w, h, direction=direction)
                # only need to check the extreme values
                pixels_to_check += [bordering_pixels[0], bordering_pixels[-1]]

            # only need to check in bounds pixels
            pixels_to_check = [(x, y) for (x, y) in pixels_to_check
                                if 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]]

            if not any(input_grid[x, y] == Color.GREY for x, y in pixels_to_check):
                # good rectangle!
                # fill in the original object with yellow
                obj[obj == Color.BLACK] = Color.YELLOW

        blit_object(output_grid, obj, background=Color.GREY)

    return output_grid


def generate_input():
    # create a 10-20x10-20 black grid
    # to make it possible to place rectangles that go offscreen,
    n = np.random.randint(10, 21)
    m = np.random.randint(10, 21)
    # add a pixel of padding, which we will remove later
    n += 1
    m += 1
    grid = np.full((n, m), Color.BLACK)

    # add 2-4 grey rectangles with hollow insides
    # each rectangle can be 3-7x3-7
    # if we can't find a space, just stop adding new rectangles
    num_rectangles = np.random.randint(2, 5)

    # store the rectangles so we can add lines to them later
    rectangles = []
    for _ in range(num_rectangles):
        r_n = np.random.randint(3, 8)
        r_m = np.random.randint(3, 8)
        rectangle = np.full((r_n, r_m), Color.GREY)
        try:
            x, y = random_free_location_for_sprite(grid, rectangle, padding=1)
        except ValueError:
            break

        # make the rectangle hollow, but mark it yellow, so we don't place another rectangle inside of it.
        # later we will convert yellow back to black
        rectangle[1:-1, 1:-1] = Color.YELLOW
        blit(grid, rectangle, x, y)
        rectangles.append((rectangle, (x, y)))

    # now draw 1-3 lines emanating from the rectangles
    # a line from another rectangle might emanate into the rectangle, so check for existing lines before adding one
    for rectangle, (x, y) in rectangles:
        num_lines = np.random.randint(1, 4)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        indices = np.random.choice(len(directions), num_lines, replace=False)
        directions = [directions[i] for i in indices]

        for direction in directions:
            # if there's already a line here, don't draw another one
            # to check, look for grey pixel within 1 pixel of the rectangle
            w, l = rectangle.shape

            bordering_pixels = find_bordering_pixels_in_direction(x, y, w, l, direction)
            bordering_pixels = np.array([(x, y) for x, y in bordering_pixels if 0 <= x < n and 0 <= y < m])
            if len(bordering_pixels) == 0:
                continue

            if any(grid[x, y] == Color.GREY for x, y in bordering_pixels):
                continue

            # now draw a line emanating outwards at a random bordering pixel
            # ignore the extreme most bordering pixels (assumes they are returned in order)
            bordering_pixels = bordering_pixels[1:-1]

            ix = np.random.choice(range(len(bordering_pixels)))
            start_pixel = bordering_pixels[ix]
            draw_line(grid, start_pixel[0], start_pixel[1], direction=direction, color=Color.GREY, stop_at_color=[Color.GREY])

    # convert yellow back to black
    grid[grid == Color.YELLOW] = Color.BLACK

    # remove the pixel of padding
    grid = grid[1:-1, 1:-1]

    return grid


def find_bordering_pixels_in_direction(x, y, w, l, direction):
    dx, dy = direction
    if dx == 1:  # right
        bordering_pixels = [(x + w, y + i) for i in range(l)]
    elif dx == -1:  # left
        bordering_pixels = [(x - 1, y + i) for i in range(l)]
    elif dy == 1:  # down
        bordering_pixels = [(x + i, y + l) for i in range(w)]
    elif dy == -1:  # up
        bordering_pixels = [(x + i, y - 1) for i in range(w)]

    return np.array(bordering_pixels)


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

