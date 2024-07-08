from common import *

import numpy as np
from typing import *

# concepts:
# direction, lines, pointing

# description:
# In the input, you will see several objects of the same color that are in an arrowhead shape and facing different directions.
# The goal is to find the directions of the arrowheads and draw lines that would represent the path they had been moving in to go in that direction.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8)

    # for each object, find the direction the arrowhead is pointing in by finding the relative mean position of colored and black pixels in the bounding box of the object
    for obj in objects:
        # find the bounding box of the object
        x, y, w, h = bounding_box(obj)

        # crop the object to extract the sprite
        sprite = crop(obj)

        # find the color of the object
        color = np.unique(obj[obj != Color.BLACK])[0]

        # find the mean position of the colored pixels
        mean_pos = np.mean(np.argwhere(sprite != Color.BLACK), axis=0)

        # find the mean position of all the black pixels
        mean_black_pos = np.mean(np.argwhere(sprite == Color.BLACK), axis=0)

        # find the direction the arrowhead is pointing in, it is from the mean position of the colored pixels to the mean position of the black pixels
        direction = np.sign(mean_black_pos - mean_pos).astype(int)

        # draw a line in the direction the arrowhead is pointing in from the corresponding corner of the bounding box
        # list the corners of the bounding box
        corners = [(x - 1, y - 1), (x + w, y - 1), (x - 1, y + h), (x + w, y + h)]
        # compute the center of the object
        center = (x + w / 2, y + h / 2)
        # if the direction of the corner from the center of the object matches the direction we want to draw a line in, then draw a line
        for corner in corners:
            # check if the corner is in the direction that the arrowhead is pointing
            vector_to_corner = np.array(corner) - np.array(center)
            if np.all(np.sign(vector_to_corner) == direction):
                draw_line(output_grid, corner[0], corner[1], length=None, color=color, direction=direction)

    return output_grid

def generate_input():
    # make a 10x10 grid as background
    grid = np.zeros((10, 10), dtype=int)

    # choose the color of the arrowheads
    color = np.random.choice(Color.NOT_BLACK)

    # make the arrowheads by making a 2x2 square then removing one of the corners randomly and placing it randomly on the grid
    for i in range(4):
        # make at arrowhead
        arrowhead = np.full((2, 2), color)
        corner = np.random.randint(4)
        arrowhead[corner // 2, corner % 2] = Color.BLACK
        
        # place it in a random free location with 1 cell padding
        x, y = random_free_location_for_sprite(grid, arrowhead, padding=1)
        blit_sprite(grid, arrowhead, x=x, y=y)
 
    return grid



    



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
