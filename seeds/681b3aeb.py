from common import *

import numpy as np
from typing import *

# concepts:
# puzzle pieces,

# description:
# In the input you will see two monochromatic objects -- "puzzle pieces"
# To make the output, fit the pieces together so that they form a single tightly-packed rectangular object. The pieces can be translated, but not rotated.

def main(input_grid):
    # Plan:
    # 1. Detect the pieces
    # 2. Consider different ways of placing them together
    # 3. Pick the way which makes them the most tightly packed, meaning that there is as little empty pixels remaining as possible

    # 1. Extract puzzle pieces
    objects = find_connected_components(input_grid, connectivity=8, background=Color.BLACK, monochromatic=True)
    assert len(objects) == 2, "There should be exactly 2 objects"
    sprites = [ crop(obj, background=Color.BLACK) for obj in objects ]
    
    width = max(sprite.shape[0] for sprite in sprites) + min(sprite.shape[0] for sprite in sprites)
    height = max(sprite.shape[1] for sprite in sprites) + min(sprite.shape[1] for sprite in sprites)
    output_grid = np.full((width, height), Color.BLACK)

    # 2. Try to fit the pieces together
    possible_placements = [ (x1, x2, y1, y2)
                           for x1 in range(width - sprites[0].shape[0] + 1)
                           for x2 in range(width - sprites[1].shape[0] + 1)
                           for y1 in range(height - sprites[0].shape[1] + 1)
                           for y2 in range(height - sprites[1].shape[1] + 1) 
                           if not collision(object1=sprites[0], object2=sprites[1], x1=x1, x2=x2, y1=y1, y2=y2) ]
    
    def score_placement(x1, x2, y1, y2):
        # We are trying to make the puzzle pieces fit together perfectly
        # Therefore, there shouldn't be very many unfilled (black) pixels remaining after we place the pieces
        # So we are minimizing the number of black pixels
        # Equivalently maximizing the negative number of black pixels
        test_canvas = np.full_like(output_grid, Color.BLACK)
        blit_sprite(test_canvas, sprites[0], x1, y1)
        blit_sprite(test_canvas, sprites[1], x2, y2)
        test_canvas = crop(test_canvas, background=Color.BLACK)
        return -np.sum(test_canvas == Color.BLACK)
    
    # pick the best one
    x1, x2, y1, y2 = max(possible_placements, key=lambda placement: score_placement(*placement))
    blit_sprite(output_grid, sprites[0], x1, y1)
    blit_sprite(output_grid, sprites[1], x2, y2)

    return crop(output_grid, background=Color.BLACK)

def generate_input():
    # Create a 2-color object and then break it up into 2 pieces
    two_color = random_sprite([2,3,4], [2,3,4], density=1, color_palette=Color.NOT_BLACK, background=Color.BLACK)
    if len(object_colors(two_color, background=Color.BLACK)) != 2:
        return generate_input()
    
    # break it up into 2 pieces
    pieces = find_connected_components(two_color, connectivity=8, background=Color.BLACK, monochromatic=True)
    if len(pieces) != 2:
        return generate_input()
    
    # convert them to sprites and then randomly place them on a big canvas
    sprites = [ crop(piece, background=Color.BLACK) for piece in pieces ]
    width, height = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((width, height), Color.BLACK)
    for sprite in sprites:
        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK)
        blit_sprite(grid, sprite, x, y, background=Color.BLACK)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
