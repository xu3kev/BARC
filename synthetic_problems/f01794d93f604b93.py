from common import *

import numpy as np
from typing import *

# concepts:
# collision detection, color mapping, symmetry, sliding objects

# description:
# The input consists of a grid containing symmetric bars and scattered colored pixels.
# The task is to move each pixel to its symmetric counterpart across the axis of symmetry (vertical/horizontal)
# while changing its color based on a given color map.
# If a pixel can't align with its counterpart, it should disappear.

color_map = {
    Color.GREEN: Color.YELLOW,
    Color.BLUE: Color.GRAY,
    Color.RED: Color.PINK,
    Color.TEAL: Color.MAROON,
    Color.YELLOW: Color.GREEN,
    Color.GRAY: Color.BLUE,
    Color.PINK: Color.RED,
    Color.MAROON: Color.TEAL
}

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    
    # Detect objects (bars and pixels)
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    bars, pixels = [], []
    for obj in objects:
        if np.all(obj == obj[0, :]) or np.all(obj == obj[:, 0]):  # Horizontal or Vertical bar
            bars.append(obj)
        else:
            pixels.append(obj)
    
    # Copy bars to the output grid
    for bar in bars:
        blit_object(output_grid, bar, background=Color.BLACK)
    
    # Detect symmetry axis (vertical or horizontal)
    if np.array_equal(input_grid[:, input_grid.shape[1]//2:], input_grid[:, :input_grid.shape[1]//2]):
        is_vertical_symmetry = True
    else:
        is_vertical_symmetry = False
    
    # Slide each pixel to its symmetric counterpart and map color
    for pixel in pixels:
        x, y = np.argwhere(pixel != Color.BLACK)[0]
        current_color = pixel[x, y]
        new_color = color_map.get(current_color, current_color)
        
        if is_vertical_symmetry:
            symmetric_y = input_grid.shape[1] - 1 - y
            if output_grid[x, symmetric_y] == Color.BLACK:
                output_grid[x, symmetric_y] = new_color
        else:
            symmetric_x = input_grid.shape[0] - 1 - x
            if output_grid[symmetric_x, y] == Color.BLACK:
                output_grid[symmetric_x, y] = new_color
    
    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Generate bars with symmetry
    num_bars = np.random.randint(2, 6)
    symmetric_bars = []
    for _ in range(num_bars):
        color = np.random.choice(list(color_map.keys()))
        if np.random.rand() > 0.5:
            # horizontal bars
            row = np.random.randint(n)
            grid[row, :] = color
            symmetric_bars.append((row, "horizontal", color))
        else:
            # vertical bars
            col = np.random.randint(m)
            grid[:, col] = color
            symmetric_bars.append((col, "vertical", color))
    
    # Generate scattered pixels
    num_pixels = np.random.randint(5, 15)
    for _ in range(num_pixels):
        color = np.random.choice(list(color_map.keys()))
        x, y = np.random.randint(n), np.random.randint(m)
        while grid[x, y] != Color.BLACK:
            x, y = np.random.randint(n), np.random.randint(m)
        grid[x, y] = color
    
    return grid