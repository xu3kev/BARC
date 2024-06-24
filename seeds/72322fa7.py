from common import *

import numpy as np
from typing import *

# concepts:
# sprites, reconstruction, alignment

# description:
# In the input you will see objects on a black grid. Some of the objects are the entirety of a sprite without anything missing. Other objects are incomplete pieces of sprites. The incomplete pieces may be not fully connected.
# To make the output, find the objects that are the entirety of a sprite. Use these objects to guide the reconstruction of the objects that are incomplete pieces of sprites. Align the missing parts of the incomplete pieces to form complete sprite representations in their respective locations.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # extract a list of candidate complete sprites from the objects, but do not verify if they are actually complete sprites yet
    candidate_complete_sprites = []
    for obj in objects:
        # crop the sprite from the object
        sprite = crop(obj)
        candidate_complete_sprites.append(sprite)

    # filter out unique sprites
    unique_sprites = []
    for sprite in candidate_complete_sprites:
        is_unique = not any( np.array_equal(sprite, other_sprite) for other_sprite in unique_sprites )
        if is_unique:
            unique_sprites.append(sprite)
    candidate_complete_sprites = unique_sprites

    # verify if the candidate complete sprites are actually complete sprites by comparing them to the other candidates and seeing if they are a component of any of the other candidates
    complete_sprites = []
    for i, sprite in enumerate(candidate_complete_sprites):
        is_complete = True
        for j, other_sprite in enumerate(candidate_complete_sprites):
            if i != j:
                # check that sprite is smaller than other_sprite
                if sprite.shape[0] > other_sprite.shape[0] or sprite.shape[1] > other_sprite.shape[1]:
                    # if not, then it cannot be a component of the other one
                    continue

                # check if sprite is a component of other_sprite
                for x in range(other_sprite.shape[0] - sprite.shape[0] + 1):
                    for y in range(other_sprite.shape[1] - sprite.shape[1] + 1):
                        if np.all(other_sprite[x:x+sprite.shape[0], y:y+sprite.shape[1]][sprite != Color.BLACK] == sprite[sprite != Color.BLACK]):
                            is_complete = False
                            break
                    if not is_complete:
                        break
            if not is_complete:
                break
        if is_complete:
            complete_sprites.append(sprite)

    # for each complete sprite, decompose it into its color components, then search for those components in the objects on the input grid to find the ones that represent incomplete sprites and reconstruct these objects
    # create an intermediary grid to reserve object locations for later reconstruction of sprite representations to account for possibility of one incomplete sprite being a possible component of multiple complete sprites
    intermediary_grid = np.zeros_like(output_grid)

    # first, reserve spots for the object representations of complete sprites and make these reservations distinct from the reservations that the object representations of incomplete sprites will get
    for i, sprite in enumerate(complete_sprites):
        for x in range(input_grid.shape[0] - sprite.shape[0] + 1):
            for y in range(input_grid.shape[1] - sprite.shape[1] + 1):
                if np.all(input_grid[x:x+sprite.shape[0], y:y+sprite.shape[1]] == sprite):
                    intermediary_grid[x:x+sprite.shape[0], y:y+sprite.shape[1]] = -1

    # reserve spots for all the other sprites
    for i, sprite in enumerate(complete_sprites):
        # count the number of reservations the current sprite has for unique reservation identifiers that can be traced back to the current sprite
        cur_sprite_reservations = 0
        # color decomposition
        sprite_colors = np.unique(sprite)
        for color in sprite_colors:
            # if the decomposition is black, then it is not meaningful
            if color == Color.BLACK:
                continue
            sprite_part = np.copy(sprite)
            sprite_part[sprite_part != color] = Color.BLACK

            # note that the list of objects will not account for the possibility that the incomplete objects have unconnected components so we need to search the grid, not the connected components
            for x in range(input_grid.shape[0] - sprite_part.shape[0] + 1):
                for y in range(input_grid.shape[1] - sprite_part.shape[1] + 1):
                    if np.all(input_grid[x:x+sprite_part.shape[0], y:y+sprite_part.shape[1]] == sprite_part):
                        # if any of the pixels are part of a complete object (have -1 as reservation number), then we should not reserve this spot
                        if np.any(intermediary_grid[x:x+sprite_part.shape[0], y:y+sprite_part.shape[1]] == -1):
                            continue
                        
                        # if all the non-black pixels in the incomplete object have the same reservations number, then we gain nothing from changing the reservation number
                        other_reservations = np.unique(intermediary_grid[x:x+sprite_part.shape[0], y:y+sprite_part.shape[1]][input_grid[x:x+sprite_part.shape[0], y:y+sprite_part.shape[1]] != 0])
                        
                        # if there is only one reservation for the non-black pixels and the reservation is not zero then we should not reserve this spot
                        if len(other_reservations) == 1 and other_reservations[0] != 0:
                            continue

                        # otherwise, we should make a reservation for the current sprite to minimize the total number of objects in the final output
                        # the reservation number should be the index of the current sprite in completed sprites plus number of reservations the current sprite has times the number of total sprites plus one
                        intermediary_grid[x:x+sprite_part.shape[0], y:y+sprite_part.shape[1]] = i + (cur_sprite_reservations * len(complete_sprites)) + 1
                        cur_sprite_reservations += 1

    # reconstruct the incomplete sprites on the output grid using the reserved spots on the intermediary grid
    # get the objects in the intermediary grid
    intermediary_objects = find_connected_components(intermediary_grid, connectivity=8, monochromatic=True)
    for obj in intermediary_objects:
        # get the bounding box of the object
        x1, y1, w, h = bounding_box(obj)

        # crop the sprite from the object
        sprite = crop(obj)

        # if the sprite is all black or already complete, then the object does not need to be reconstructed
        if np.all(sprite == 0) or np.all(sprite == -1):
            continue

        # get the index of the sprite in the complete sprites list
        sprite_index = np.unique(sprite)[0]

        # get the complete sprite
        complete_sprite = complete_sprites[(sprite_index - 1) % len(complete_sprites)]

        # make sure the reserved space is not smaller than the sprite
        if w < complete_sprite.shape[0] or h < complete_sprite.shape[1]:
            continue

        # find all places where a object respresentation of the complete sprite can fit in the reserved space
        for x1 in range(x1, x1 + w - complete_sprite.shape[0] + 1):
            for y1 in range(y1, y1 + h - complete_sprite.shape[1] + 1):
                # if the whole region matches the sprite index, then we can reconstruct the object representation of the sprite here
                if np.all(intermediary_grid[x1:x1+complete_sprite.shape[0], y1:y1+complete_sprite.shape[1]] == sprite_index):
                    # reconstruct the incomplete object representation of the sprite
                    blit(output_grid, complete_sprite, x1, y1)
                    # erase the reservations for these pixels
                    intermediary_grid[x1:x1+complete_sprite.shape[0], y1:y1+complete_sprite.shape[1]] = 0                   

    return output_grid


def generate_input():
    # make a black grid of random size
    n = np.random.randint(12, 23)
    m = np.random.randint(12, 23)
    grid = np.zeros((n, m), dtype=int)

    # make a random number of complete sprites as guides for incomplete sprites and object representations
    num_complete_sprites = np.random.randint(1, 4)

    # make the complete sprites and store them in a list for later use
    complete_sprites = []
    for _ in range(num_complete_sprites):
        # choose between vertical, horizontal, or radial symmetry
        symmetry = np.random.choice(["vertical", "horizontal", "radial"])

        # make a random sprite with the chosen symmetry
        sprite = random_sprite(list(range(1, 4)), list(range(1, 4)), symmetry=symmetry, color_palette=Color.NOT_BLACK)

        # make sure the sprite has more than 1 color other than black
        while len(np.unique(sprite)) < 3:
            sprite = random_sprite(list(range(1, 4)), list(range(1, 4)), symmetry=symmetry, color_palette=Color.NOT_BLACK)
        complete_sprites.append(sprite)

    # for each complete sprite, place an complete object representation in a random location on the grid and place a random number of incomplete object representations based on the complete sprite in other random locations
    for sprite in complete_sprites:
        # if there is not a free location for the complete sprite, then skip it
        try:
            x, y = random_free_location_for_object(grid, sprite, padding=2, padding_connectivity=8)
            blit(grid, sprite, x, y)
        except:
            continue

        # decompose the sprite into its color components
        sprite_colors = np.unique(sprite)

        # remove black from the color components
        sprite_colors = sprite_colors[sprite_colors != Color.BLACK]

        # place incomplete object representations based on the complete sprite
        for _ in range(np.random.randint(1, 4)):
            # choose a random color from the sprite to represent the incomplete sprite
            color = np.random.choice(sprite_colors)

            # make an incomplete sprite with the chosen color based on the complete sprite
            incomplete_sprite = np.copy(sprite)
            incomplete_sprite[incomplete_sprite != color] = Color.BLACK

            # place the incomplete sprite in a random location on the grid
            # if there is not a free location for the incomplete sprite, then skip it
            try:
                x, y = random_free_location_for_object(grid, incomplete_sprite, padding=2, padding_connectivity=8)
                blit(grid, incomplete_sprite, x, y)
            except:
                pass

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)