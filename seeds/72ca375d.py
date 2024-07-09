from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, sprites

# description:
# In the input you will see several objects. One object represents a symmetic sprite. All the other objects represent non-symmetric sprites.
# The goal is to find the symmetric sprite and return it.

def main(input_grid):
    # find the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8)

    # crop out the sprites from the objects
    sprites = [crop(obj) for obj in objects]

    # find the symmetric sprite
    symmetric_sprite = None
    for sprite in sprites:
      # check if the sprite is radially symmetric
      if np.array_equal(sprite, np.rot90(sprite, 1)):
        symmetric_sprite = sprite
        break
      # check if the sprite is vertically symmetric
      elif np.array_equal(sprite, np.fliplr(sprite)):
        symmetric_sprite = sprite
        break
      # check if the sprite is horizontally symmetric
      elif np.array_equal(sprite, np.flipud(sprite)):
        symmetric_sprite = sprite
        break
      # check if the sprite is diagonally symmetric
      elif np.array_equal(sprite, sprite.T) or np.array_equal(np.flipud(sprite), np.fliplr(sprite)):
        symmetric_sprite = sprite
        break

    return symmetric_sprite

  

def generate_input():
    # make a black 10x10 grid as background
    grid = np.zeros((10, 10), dtype=int)

    # add a symmetric sprite:
    # choose the color of the sprite
    color = np.random.choice(Color.NOT_BLACK)

    # choose the sidelength of the sprite
    side_length = np.random.randint(2, 8)

    # choose the width of the sprite to be either 2 or the side_length
    width = np.random.choice([2, side_length])

    # choose the height of the sprite to be whatever is left
    height = side_length if width == 2 else 2

    # choose the symmetry that the sprite will have
    symmetry = np.random.choice(['vertical', 'horizontal', 'diagonal', 'radial'])

    # override width and height if the symmetry is radial or diagonal
    if symmetry in ['radial', 'diagonal']:
        width = height = np.random.randint(2, 5)

    # make the sprite
    symmetric_sprite = random_sprite(width, height, symmetry=symmetry, color_palette=[color], connectivity=8)

    # place the sprite randomly on the grid
    x, y = random_free_location_for_sprite(grid, symmetric_sprite, padding=1)
    blit_sprite(grid, symmetric_sprite, x=x, y=y)

    # add some non-symmetric sprites:
    for _ in range(np.random.randint(3, 6)):
        # choose the color of the sprite
        color = np.random.choice(Color.NOT_BLACK)

        # choose the sidelength of the sprite
        side_length = np.random.randint(3, 8)

        # choose the width of the sprite to be either 2 or the side_length
        width = np.random.choice([2, side_length])

        # choose the height of the sprite to be whatever is left
        height = side_length if width == 2 else 2

        # make the sprite
        non_symmetric_sprite = random_sprite(width, height, symmetry="not_symmetric", color_palette=[color], connectivity=8)

        # place the sprite randomly on the grid if there is space
        try:
          x, y = random_free_location_for_sprite(grid, non_symmetric_sprite, padding=1)
          blit_sprite(grid, non_symmetric_sprite, x=x, y=y)
        except:
          pass

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
