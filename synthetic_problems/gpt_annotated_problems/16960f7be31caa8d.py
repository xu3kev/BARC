from common import *

import numpy as np
from typing import *

# concepts:
# rectangular cells, color guide, connecting same color, flood fill

# description:
# In the input you will see a grid divided into four quadrants by black lines. Each quadrant contains a different color.
# To make the output:
# 1. Identify the quadrant with the most pixels of its color.
# 2. Use that color to flood fill any adjacent quadrants that share at least one non-black pixel along their border.
# 3. Remove the black dividing lines between filled quadrants.
# The result will be a larger connected region of the dominant color.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # Find the black dividing lines
    for i in range(input_grid.shape[0]):
        if np.all(input_grid[i, :] == Color.BLACK):
            x_separator = i
            break
    for i in range(input_grid.shape[1]):
        if np.all(input_grid[:, i] == Color.BLACK):
            y_separator = i
            break
    
    # Define the quadrants
    quadrants = [
        (0, 0, x_separator, y_separator),
        (0, y_separator, x_separator, input_grid.shape[1]),
        (x_separator, 0, input_grid.shape[0], y_separator),
        (x_separator, y_separator, input_grid.shape[0], input_grid.shape[1])
    ]
    
    # Find the dominant color and its quadrant
    max_pixels = 0
    dominant_color = None
    dominant_quadrant = None
    for q in quadrants:
        quadrant = input_grid[q[0]:q[2], q[1]:q[3]]
        colors, counts = np.unique(quadrant[quadrant != Color.BLACK], return_counts=True)
        if len(counts) > 0 and counts[0] > max_pixels:
            max_pixels = counts[0]
            dominant_color = colors[0]
            dominant_quadrant = q
    
    # Flood fill adjacent quadrants
    filled_quadrants = [dominant_quadrant]
    to_fill = [dominant_quadrant]
    while to_fill:
        current = to_fill.pop(0)
        for q in quadrants:
            if q not in filled_quadrants:
                # Check if quadrants are adjacent and share a non-black pixel
                if (current[0] == q[2] or current[2] == q[0]) and np.any((input_grid[current[2]-1, max(current[1], q[1]):min(current[3], q[3])] != Color.BLACK) & 
                                                                         (input_grid[q[0], max(current[1], q[1]):min(current[3], q[3])] != Color.BLACK)):
                    output_grid[q[0]:q[2], q[1]:q[3]][output_grid[q[0]:q[2], q[1]:q[3]] != Color.BLACK] = dominant_color
                    filled_quadrants.append(q)
                    to_fill.append(q)
                elif (current[1] == q[3] or current[3] == q[1]) and np.any((input_grid[max(current[0], q[0]):min(current[2], q[2]), current[3]-1] != Color.BLACK) & 
                                                                           (input_grid[max(current[0], q[0]):min(current[2], q[2]), q[1]] != Color.BLACK)):
                    output_grid[q[0]:q[2], q[1]:q[3]][output_grid[q[0]:q[2], q[1]:q[3]] != Color.BLACK] = dominant_color
                    filled_quadrants.append(q)
                    to_fill.append(q)
    
    # Remove black lines between filled quadrants
    if len(filled_quadrants) > 1:
        min_x = min(q[0] for q in filled_quadrants)
        max_x = max(q[2] for q in filled_quadrants)
        min_y = min(q[1] for q in filled_quadrants)
        max_y = max(q[3] for q in filled_quadrants)
        output_grid[min_x:max_x, min_y:max_y][output_grid[min_x:max_x, min_y:max_y] == Color.BLACK] = dominant_color
    
    return output_grid

def generate_input() -> np.ndarray:
    # Make a grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK)
    
    # Choose random positions for separators
    x_separator = np.random.randint(n // 3, 2 * n // 3)
    y_separator = np.random.randint(m // 3, 2 * m // 3)
    
    # Define quadrants
    quadrants = [
        (0, 0, x_separator, y_separator),
        (0, y_separator + 1, x_separator, m),
        (x_separator + 1, 0, n, y_separator),
        (x_separator + 1, y_separator + 1, n, m)
    ]
    
    # Fill quadrants with different colors
    colors = random.sample(Color.NOT_BLACK, 4)
    for (x1, y1, x2, y2), color in zip(quadrants, colors):
        grid[x1:x2, y1:y2] = color
    
    return grid