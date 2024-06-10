from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide

# description:
# In the input you will see a pretty big grid divided into four axis-aligned quadrants (but there might be different sizes), each of which is separated by at least 1 row/column of black. All the quadrants contain random pixels, and all quadrants except for one have the same color
# To make the output, find the quadrant with a different color, and copy only that quadrant to the output, producing a smaller grid

def main(input_grid: np.ndarray) -> np.ndarray:
    # break the input up into quadrants
    # remember they are different sizes, but they are all separated by at least 2 rows/columns of black
    # we do this by computing the x, y coordinates of separators
    for i in range(input_grid.shape[0]):
        if np.all(input_grid[i, :] == Color.BLACK):
            x_separator = i
            break
    for i in range(input_grid.shape[1]):
        if np.all(input_grid[:, i] == Color.BLACK):
            y_separator = i
            break
    
    quadrants = [ input_grid[:x_separator, :y_separator],
                  input_grid[:x_separator, y_separator:],
                  input_grid[x_separator:, :y_separator],
                  input_grid[x_separator:, y_separator:] ]
    
    # check that each of them is monochromatic (only one color that isn't black)
    colors = [ np.unique(quadrant[quadrant != Color.BLACK]) for quadrant in quadrants ]
    for color in colors:
        assert len(color) == 1, "Quadrant has more than one color"

    for color, quadrant in zip(colors, quadrants):
        color_frequency = sum(other_color == color for other_color in colors)
        if color_frequency == 1:
            output_grid = quadrant

            # we have to crop the output grid to remove any extraneous black rows/columns
            output_grid = crop(output_grid, background=Color.BLACK)

            break

    return output_grid



def generate_input() -> np.ndarray:
    
    # pick a pair of colors, one of which is going to fill 3 quadrants, and the other will fill 1
    popular_color, unique_color = random.sample(Color.NOT_BLACK, 2)

    # make a grid
    n, m = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.zeros((n, m), dtype=int)

    # pick a random size for the first quadrant (all other quadrant sizes follow from this)
    x_size, y_size = np.random.randint(6, n-6), np.random.randint(6, m-6)

    quadrants = [ grid[:x_size, :y_size],
                  grid[:x_size, y_size:],
                  grid[x_size:, :y_size],
                  grid[x_size:, y_size:] ]
    unique_quadrant = random.choice(quadrants)
    for quadrant in quadrants:
        target_color = popular_color if quadrant is not unique_quadrant else unique_color
        # fill a random 70% of the quadrant with the target color
        for i in range(quadrant.shape[0]):
            for j in range(quadrant.shape[1]):
                if random.random() < 0.7:
                    quadrant[i, j] = target_color
        
    # add black separators
    separator_width, separator_height = np.random.randint(2, 4), np.random.randint(2, 4)
    grid[x_size:x_size+separator_width, :] = Color.BLACK
    grid[:, y_size:y_size+separator_height] = Color.BLACK

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)