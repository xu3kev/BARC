from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, collision detection, patterns

# description:
# In the input, you will see a red pixel, a blue pixel, and a teal pixel.
# To make the output:
# 1. Draw a yellow line from the red pixel towards the blue pixel, stopping if it hits the edge of the grid or the teal pixel.
# 2. Draw a pink line from the blue pixel towards the red pixel, stopping if it hits the edge of the grid, the teal pixel, or the yellow line.
# 3. If the yellow and pink lines touch (including at their endpoints), draw a green pixel at each point where they touch.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find positions of colored pixels
    red_pos = np.argwhere(input_grid == Color.RED)[0]
    blue_pos = np.argwhere(input_grid == Color.BLUE)[0]
    teal_pos = np.argwhere(input_grid == Color.TEAL)[0]
    
    # Calculate direction from red to blue
    direction_red_to_blue = np.sign(blue_pos - red_pos)
    
    # Draw yellow line from red towards blue
    draw_line(output_grid, red_pos[0], red_pos[1], length=None, color=Color.YELLOW, 
              direction=direction_red_to_blue, stop_at_color=[Color.TEAL])
    
    # Calculate direction from blue to red
    direction_blue_to_red = np.sign(red_pos - blue_pos)
    
    # Draw pink line from blue towards red
    draw_line(output_grid, blue_pos[0], blue_pos[1], length=None, color=Color.PINK, 
              direction=direction_blue_to_red, stop_at_color=[Color.TEAL, Color.YELLOW])
    
    # Find points where yellow and pink touch
    yellow_pixels = np.argwhere(output_grid == Color.YELLOW)
    pink_pixels = np.argwhere(output_grid == Color.PINK)
    
    for y_pixel in yellow_pixels:
        for p_pixel in pink_pixels:
            if np.abs(y_pixel - p_pixel).sum() <= 1:  # Adjacent or same position
                output_grid[y_pixel[0], y_pixel[1]] = Color.GREEN
                output_grid[p_pixel[0], p_pixel[1]] = Color.GREEN
    
    return output_grid

def generate_input():
    n, m = np.random.randint(8, 15), np.random.randint(8, 15)
    grid = np.full((n, m), Color.BLACK)
    
    # Place red, blue, and teal pixels
    colors = [Color.RED, Color.BLUE, Color.TEAL]
    for color in colors:
        while True:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                break
    
    return grid