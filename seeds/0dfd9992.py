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

    w, h = input_grid.shape

    # Identify the translational symmetry
    h_period = detect_horizontal_periodicity(input_grid, ignore_color=Color.BLACK)
    v_period = detect_vertical_periodicity(input_grid, ignore_color=Color.BLACK)

    # Reconstruct the sprite by ignoring the black pixels and exploiting the periodicity
    sprite = np.full((h_period, v_period), Color.BLACK)
    for x in range(h_period):
        for y in range(v_period):
            possible_inputs = [input_grid[x + i*h_period, y + j*v_period] for i in range(w//h_period) for j in range(h//v_period)]
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
