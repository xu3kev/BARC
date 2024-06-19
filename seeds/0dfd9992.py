from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, translational symmetry

# description:
# In the input you will see a translationally symmetric pattern randomly occluded by black pixels.
# To make the output, remove the occluding black pixels to reveal the translationally symmetric pattern.

def main(input_grid):
    # Plan:
    # 1. Find the periodicity of the translational symmetry, in both horizontal and vertical directions
    # 2. Reconstruct the sprite by ignoring the black pixels and exploiting the periodicity
    # 3. Make the output by tiling the sprite infinitely in all directions

    # Identify the horizontal period of translational symmetry
    # input_grid[x, y] == input_grid[x + i*h_period, y] for all x, y, i (where the pixels aren't black)
    for h_period in range(1, input_grid.shape[0]):
        pattern = input_grid[:, :h_period]
        h_repetitions = input_grid.shape[0] // h_period

        success = True
        for i in range(1, h_repetitions):
            sliced_input = input_grid[:, i*h_period:(i+1)*h_period]
            sliced_pattern = pattern[:sliced_input.shape[0], :sliced_input.shape[1]]
            # Check that they are equal except where one of them is black
            if np.all((sliced_input == sliced_pattern) | (sliced_input == Color.BLACK) | (sliced_pattern == Color.BLACK)):
                # Update the pattern to include the any new nonblack pixels
                sliced_pattern[sliced_input != Color.BLACK] = sliced_input[sliced_input != Color.BLACK]
            else:
                success = False
                break
        if success:
            break
    
    # Identify the vertical period of translational symmetry
    # input_grid[x, y] == input_grid[x, y + i*v_period] for all x, y, i (where the pixels aren't black)
    for v_period in range(1, input_grid.shape[1]):
        pattern = input_grid[:v_period, :]
        v_repetitions = input_grid.shape[1] // v_period

        success = True
        for i in range(1, v_repetitions):
            sliced_input = input_grid[i*v_period:(i+1)*v_period, :]
            sliced_pattern = pattern[:sliced_input.shape[0], :sliced_input.shape[1]]
            # Check that they are equal except where one of them is black
            if np.all((sliced_input == sliced_pattern) | (sliced_input == Color.BLACK) | (sliced_pattern == Color.BLACK)):
                # Update the pattern to include the any new nonblack pixels
                sliced_pattern[sliced_input != Color.BLACK] = sliced_input[sliced_input != Color.BLACK]
            else:
                success = False
                break
        if success:
            break

    # Reconstruct the sprite by ignoring the black pixels and exploiting the periodicity
    sprite = np.full((h_period, v_period), Color.BLACK)
    for x in range(h_period):
        for y in range(v_period):
            possible_inputs = [input_grid[x + i*h_period, y + j*v_period] for i in range(h_repetitions) for j in range(v_repetitions)]
            nonblack_inputs = [c for c in possible_inputs if c != Color.BLACK]
            if len(nonblack_inputs) == 0:
                sprite[x, y] = Color.BLACK
            else:
                sprite[x, y] = nonblack_inputs[0]
    
    # Make the output by tiling the sprite infinitely in all directions
    output_grid = np.full((input_grid.shape[0], input_grid.shape[1]), Color.BLACK)
    for x in range(0, input_grid.shape[0], h_period):
        for y in range(0, input_grid.shape[1], v_period):
            blit(output_grid, sprite, x, y)
    
    return output_grid


def generate_input():
    # Make a random large canvas
    grid = np.full((np.random.randint(15, 30), np.random.randint(15, 30)), Color.BLACK)

    # Make the basic sprite
    w, h = random.randint(3, 8), random.randint(3, 8)
    sprite = random_sprite(w, h, density=1, color_palette=Color.NOT_BLACK)

    # Place the sprite in the canvas
    for x in range(0, grid.shape[0], w):
        for y in range(0, grid.shape[1], h):
            blit(grid, sprite, x, y)
    
    # Create random occluders
    n_occluders = random.randint(1, 5)
    for _ in range(n_occluders):
        x, y = random.randint(0, grid.shape[0]), random.randint(0, grid.shape[1])
        w, h = random.randint(3, 7), random.randint(3, 7)
        occluder = np.full((w, h), Color.BLACK)
        blit(grid, occluder, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
