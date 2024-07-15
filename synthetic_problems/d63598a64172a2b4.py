from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, sliding objects, uniqueness

# description:
# In the input, you will see a grid containing colored pixels and horizontal or vertical bars
# Move each colored pixel to the bar that has the same color.
# If a colored pixel doesn't have a corresponding bar, it should remain in its original position.
# If a bar has a unique color (in the input grid or after pixels are moved), uncover the whole grid to reveal the unique bar color.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    
    # each object is either a bar or pixel, all with the same color
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # separate the bars from the pixels
    bars, pixels = [], []
    for obj in objects:
        w, h = crop(obj).shape
        if w == input_grid.shape[0] or h == input_grid.shape[1]:
            bars.append(obj)
        else:
            pixels.append(obj)
    
    # move pixels to the corresponding colored bar
    for pixel in pixels:
        color = np.unique(pixel)[1]  # Extract the color of the pixel (excluding the background color).
        matching_bars = [bar for bar in bars if np.unique(bar)[1] == color]

        # if there is no matching bar, place the pixel back at its original position
        if len(matching_bars) == 0:
            blit_object(output_grid, pixel, background=Color.BLACK)
        else:
            possible_displacements = [(slide_distance * dx, slide_distance * dy)
                                      for slide_distance in range(max(input_grid.shape))
                                      for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            for dx, dy in possible_displacements:
                new_pixel = translate(pixel, dx, dy, background=Color.BLACK)
                if contact(object1=matching_bars[0], object2=new_pixel):
                    blit_object(output_grid, new_pixel, background=Color.BLACK)
                    break
    
    # copy the bars to the output grid
    for bar in bars:
        blit_object(output_grid, bar, background=Color.BLACK)
    
    # Detect if there's a unique color in the grid
    unique_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(output_grid == color) == 1:
            unique_color = color
            break

    # If there's a unique color, remove all occlusions
    if unique_color is not None:
        output_grid = input_grid

    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    
    # separately generate canvas for bars and pixels, so that we can put the bars on top of the pixels
    just_the_bars = np.zeros((n, m), dtype=int)
    just_the_pixels = np.zeros((n, m), dtype=int)

    n_bars = np.random.randint(1, 5)

    # make sure that every bar has a different color
    bar_colors = random.sample(Color.NOT_BLACK, n_bars)

    for bar in range(n_bars):
        color = bar_colors[bar]
        horizontal_or_vertical = np.random.choice(["horizontal", "vertical"])
        if horizontal_or_vertical == "horizontal":
            x = np.random.randint(0, n)
            just_the_bars[x, :] = color
        else:
            y = np.random.randint(0, m)
            just_the_bars[:, y] = color

        n_pixels = np.random.randint(1, 5)
        for _ in range(n_pixels):
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            just_the_pixels[x, y] = color

    # sample a few pixels that aren't the same color as any of the bars
    not_a_bar_color = set(Color.NOT_BLACK) - set(bar_colors)
    n_distracter_pixels = np.random.randint(1, 5)
    for _ in range(n_distracter_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        just_the_pixels[x, y] = np.random.choice(list(not_a_bar_color))

    # create random occluders
    n_occluders = random.randint(1, 5)
    for _ in range(n_occluders):
        x, y = random.randint(0, n), random.randint(0, m)
        w, h = random.randint(2, 4), random.randint(2, 4)
        occluder_sprite = np.full((w, h), Color.BLACK)
        blit_sprite(just_the_pixels, occluder_sprite, x, y)

    # put the bars on top of the pixels by copying them on top
    grid = just_the_pixels.copy()
    blit_object(grid, just_the_bars, background=Color.BLACK)
    
    return grid