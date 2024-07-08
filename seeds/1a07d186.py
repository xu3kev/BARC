from common import *

import numpy as np
from typing import *

# concepts:
# collision detection, sliding objects, horizontal/vertical bars

# description:
# In the input you will see horizontal/vertical bars and individual coloured pixels sprinkled on a black background
# Move each colored pixel to the bar that has the same colour until the pixel touches the bar.
# If a colored pixel doesn't have a corresponding bar, it should be deleted.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)

    # each object is either a bar or pixel, all uniform color
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # separate the bars from the pixels
    bars, pixels = [], []
    for obj in objects:
        w, h = crop(obj).shape
        if w == input_grid.shape[0] or h == input_grid.shape[1]:
            bars.append(obj)
        else:
            pixels.append(obj)
    
    # copy the bars to the output grid
    for bar in bars:
        blit_object(output_grid, bar, background=Color.BLACK)
    
    # slide each pixel until it just barely touches the bar with the matching color
    for pixel in pixels:
        color = np.unique(pixel)[1]
        matching_bars = [bar for bar in bars if np.unique(bar)[1] == color]

        # if there is no matching bar, delete the pixel
        if len(matching_bars) == 0:
            continue

        # consider sliding in the 4 cardinal directions, and consider sliding as far as possible
        possible_displacements = [ (slide_distance*dx, slide_distance*dy)
                                   for slide_distance in range(max(input_grid.shape))
                                   for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)] ]
        for dx, dy in possible_displacements:
            new_pixel = translate(pixel, dx, dy, background=Color.BLACK)
            if contact(object1=matching_bars[0], object2=new_pixel):
                blit_object(output_grid, new_pixel, background=Color.BLACK)
                break
    
    return output_grid



def generate_input() -> np.ndarray:

    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    
    # separately generate canvas for bars and pixels, so that we can put the bars on top of the pixels
    just_the_bars = np.zeros((n, m), dtype=int)
    just_the_pixels = np.zeros((n, m), dtype=int)

    n_bars = np.random.randint(1, 5)

    # make sure that every bar has a different color
    bar_colors = random.sample(Color.NOT_BLACK, n_bars)

    horizontal_or_vertical = np.random.choice(["horizontal", "vertical"])
    for bar in range(n_bars):
        color = bar_colors[bar]

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

    # put the bars on top of the pixels by copying them on top
    grid = just_the_pixels.copy()
    blit_object(grid, just_the_bars, background=Color.BLACK)
    # Equivalent to:
    # grid[just_the_bars != Color.BLACK] = just_the_bars[just_the_bars != Color.BLACK]
    

    return grid


        






    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)