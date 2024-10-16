from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, occlusion

# description:
# In the input you will see a left-right symmetric monochromatic object occluded by a colored rectangle
# To make the output, remove the colored rectangle and fill in the missing parts of the object to make it left-right symmetric

def main(input_grid):
    # Plan:
    # 1. Extract and separate the rectangle from the symmetric object
    # 2. Find the left-right symmetry
    # 3. Fill in the missing parts of the object

    background_color = Color.BLACK

    # Each object has a different color, so we can look at connected components by color
    objects = detect_objects(input_grid, monochromatic=True, connectivity=8, background=background_color)
    sprites = [ crop(obj, background=Color.BLACK) for obj in objects ]
    # Find the rectangle
    for obj, sprite in zip(objects, sprites):
        # the rectangle will be completely filled, so we can check if its total area is the whole rectangular region
        if sprite.shape[0] * sprite.shape[1] == np.sum(sprite != Color.BLACK):
            rectangle = obj
            break

    # Find the color of the rectangle, because it is the occluder
    rectangle_color = object_colors(rectangle, background=background_color)[0]
    
    # Delete the rectangle
    rectangle_mask = rectangle != Color.BLACK
    output_grid = input_grid.copy()
    output_grid[rectangle_mask] = Color.BLACK

    # Find the symmetry
    # The occluder is rectangle_color, so we ignore it. In contrast, Color.BLACK is places where the object *actually* isn't located, so we can't ignore that.
    mirrors = detect_mirror_symmetry(input_grid, ignore_colors=[rectangle_color], background=Color.BLACK)

    # Mirror each colored pixel
    for x, y in np.argwhere(output_grid != Color.BLACK):
        for mirror in mirrors:
            source_color = output_grid[x,y]
            destination = mirror.apply(x, y)
            output_grid[destination] = source_color

    return output_grid


def generate_input():
    # Create a medium sized grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    object_color, rectangle_color = random.sample(list(Color.NOT_BLACK), 2)

    sprite = random_sprite(np.random.randint(5, n-2), np.random.randint(5, m-2), density=0.5, symmetry="horizontal", color_palette=[object_color])
    rectangle = np.full((np.random.randint(2, 5), np.random.randint(2, 5)), rectangle_color)

    sprite_x, sprite_y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x=sprite_x, y=sprite_y)

    # Find a random place for the rectangle that is NOT free (because the rectangle occludes the sprite)
    while True:
        rectangle_x, rectangle_y = np.random.randint(0, n-rectangle.shape[0]), np.random.randint(0, m-rectangle.shape[1])
        if collision(object1=grid, object2=rectangle, x2=rectangle_x, y2=rectangle_y, background=Color.BLACK):
            # Equivalently, could have done:
            # collision(object1=sprite, object2=rectangle, x1=sprite_x, y1=sprite_y, x2=rectangle_x, y2=rectangle_y)
            break
    blit_sprite(grid, rectangle, x=rectangle_x, y=rectangle_y, background=Color.BLACK)
    return grid
    



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
