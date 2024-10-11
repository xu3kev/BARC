from common import *

import numpy as np
from typing import *

# concepts:
# puzzle pieces, rotation

# description:
# In the input you will see a red object with holes in it, and several multicolored 3x3 "puzzle pieces"
# To make the output, crop to just the red object and then put each puzzle piece in the red object so that the red pixels in the puzzle piece perfectly fit into the holes in the red object. You can rotate and translate the puzzle pieces to make them fit.

def main(input_grid):
    # Plan:
    # 1. Detect the object, separating the puzzle pieces from the red object with holes
    # 2. Crop to just the red object
    # 3. Put each puzzle piece so that its red pixels perfectly overlay holes in the red object (considering translations and rotations)

    # 1. Separate puzzle pieces from the red object (remembering that puzzle pieces might have some red in them also: they are not monochromatic---but the red thing is fully red)
    objects = find_connected_components(input_grid, connectivity=8, background=Color.BLACK, monochromatic=False)
    red_objects = [ obj for obj in objects if set(object_colors(obj, background=Color.BLACK)) == {Color.RED} ]
    puzzle_pieces = [ obj for obj in objects if set(object_colors(obj, background=Color.BLACK)) != {Color.RED} ]

    assert len(red_objects) == 1, "There should be exactly one fully red object"
    red_object = red_objects[0]

    # 2. The output begins by cropping to just the red object
    output_grid = crop(red_object, background=Color.BLACK)

    # 3. Put each puzzle piece so that its red pixels perfectly overlay holes in the red object
    # Put in the pieces which have the most red first (otherwise a small puzzle piece might go in a big hole)
    puzzle_pieces.sort(key=lambda piece: np.sum(piece == Color.RED), reverse=True)

    for puzzle_piece in puzzle_pieces:
        # Extract just the sprite of this piece, and then figure out where it should go, including its position and rotation
        piece_sprite = crop(puzzle_piece, background=Color.BLACK)
        possible_sprites = [ piece_sprite, np.rot90(piece_sprite), np.rot90(piece_sprite, k=2), np.rot90(piece_sprite, k=3) ]

        # A placement solution is a tuple (x, y, sprite) where x, y is the top-left corner of the rotated sprite
        possible_solutions = [ (x, y, sprite)
                              for sprite in possible_sprites
                              for x in range(output_grid.shape[0] - piece_sprite.shape[0] + 1)
                              for y in range(output_grid.shape[1] - piece_sprite.shape[1] + 1) ]
        
        # Filter placement solutions to only those where the red pixels of the piece fit into the holes of the red object
        def valid_solution(x, y, sprite):
            # Make a canvas to try putting down the sprite
            test_canvas = np.full_like(output_grid, Color.BLACK)
            blit_sprite(test_canvas, sprite, x, y)
            # Check if every red pixel in the placed test object is also red in the red object
            red_pixels = [ (x, y) for x, y in np.argwhere(test_canvas == Color.RED) ]
            return all( output_grid[red_x, red_y] == Color.BLACK for red_x, red_y in red_pixels )
                
        possible_solutions = [ solution for solution in possible_solutions if valid_solution(*solution) ]
        if len(possible_solutions) == 0:
            assert False, "No solution found for puzzle piece"

        # Pick the first solution and blit the sprite into the output grid
        x, y, sprite = list(possible_solutions)[0]
        blit_sprite(output_grid, sprite, x, y)
    
    return output_grid

def generate_input():
    # Create a red canvas and some pieces that have red in them. Then place the pieces randomly (remembering to rotate) and punch black holes where they are red

    canvas_width, canvas_height = np.random.randint(10, 20), np.random.randint(10, 20)
    red_canvas = np.full((canvas_width, canvas_height), Color.RED)


    n_pieces = np.random.randint(2, 5)
    pieces = []
    for _ in range(n_pieces):
        # puzzle pieces are 3x3 and contain both red and non-red pixels
        # treat the background as red, and give it a single color for the color palette, so that it ends up with just red and another color
        piece_width, piece_height = 3, 3
        non_red_color = random.choice([ color for color in Color.NOT_BLACK if color != Color.RED ])
        piece = random_sprite(piece_width, piece_height, connectivity=8, color_palette=[non_red_color], background=Color.RED)
        pieces.append(piece)

        # the piece is randomly rotated and randomly placed
        rotated_piece = np.rot90(piece, k=np.random.randint(0, 4))        
        x, y = random_free_location_for_sprite(red_canvas, rotated_piece, background=Color.RED)

        # punch holes in the red canvas where the piece is red
        red_pixels = np.argwhere(rotated_piece == Color.RED)
        for dx, dy in red_pixels:
            red_canvas[x + dx, y + dy] = Color.BLACK
        
    # create the actual input grid, which contains the red canvas and the pieces randomly arranged
    width, height = np.random.randint(canvas_width+3, 30+1), np.random.randint(canvas_height+3, 30+1)
    grid = np.full((width, height), Color.BLACK)

    x, y = random_free_location_for_sprite(grid, red_canvas, background=Color.BLACK)
    blit_sprite(grid, red_canvas, x, y)

    for piece in pieces:
        x, y = random_free_location_for_sprite(grid, piece, background=Color.BLACK)
        blit_sprite(grid, piece, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
