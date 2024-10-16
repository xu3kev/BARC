from common import *

import numpy as np
from typing import *

# concepts:
# scaling, pattern matching

# description:
# In the input you should see three objects, two of which are the same pattern but different sizes and colors. The third object is a different pattern.
# To make the output, you need to find the two objects that are the same pattern but different sizes and colors.
# Return the smaller object in the same pattern.

def main(input_grid):
    # Determine the background color, which is the most common color in the grid
    colors = np.unique(input_grid)
    background = colors[np.argmax([np.sum(input_grid == c) for c in colors])]
    object_colors = [c for c in colors if c != background]

    # Extract the objects, the object is a pattern of same color
    objects = find_monochromatic_sprite(input_grid, color_palate=object_colors, background=background)
    object_list = []
    for object in objects:
        x, y, w, h = bounding_box(object, background=background)
        cropped_object = crop(object, background=background)
        object_color = np.unique(cropped_object)
        object_color = object_color[object_color != background][0] 
        object_list.append({"x": x, "y": y, "w": w, "h": h, "pattern": cropped_object, "color": object_color})
    
    output_grid_candidates = []
    # Iterate all candidate objects
    for object in object_list:
        # Iterate all scale factors
        for scale_factor in range(2, 4):
            # Scale the object
            scaled_pattern = scale_sprite(object["pattern"], scale_factor)
            
            # Check if the the other two objects can partially perfect fit scaled object can partially fit 
            for other_object in object_list:
                if other_object == object:
                    continue
                cur_pattern = other_object["pattern"].copy()
                cur_w, cur_h = other_object["w"], other_object["h"]
                # iterate all pixels in the scaled object
                for x, y in np.argwhere(scaled_pattern):
                    # Check if the object can partially perfect fit the scaled object
                    if x + cur_w <= scaled_pattern.shape[0] and y + cur_h <= scaled_pattern.shape[1]:
                        partial_scaled_grid = scaled_pattern[x : x + cur_w, y : y + cur_h]
                        
                        # Change the color of the bigger object to the smaller object for comparison
                        cur_pattern[cur_pattern == other_object["color"]] = object["color"]

                        # If it fit perfectly, return the output grid
                        if np.all(partial_scaled_grid == cur_pattern):
                            # Find the object we want
                            output_grid_candidates.append(object["pattern"])
                            break

    # Check if the generated input grid is valid
    assert len(output_grid_candidates) == 1, "Should only have one output grid candidate"

    output_grid = output_grid_candidates[0]
    return output_grid

def generate_input():
    # get color for background and three objects
    colors = np.random.choice(Color.NOT_BLACK, 4, replace=False)
    background, object_small, object_big, object_other = colors

    # Create background grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), background)

    # Create different two pattern
    n1, m1 = np.random.randint(3, 6), np.random.randint(3, 6)
    n2, m2 = np.random.randint(3, 6), np.random.randint(3, 6)

    pattern_small = random_sprite(n=n1, m=m1, color_palette=[object_small], background=background, connectivity=8)
    pattern_other = random_sprite(n=n2, m=m2, color_palette=[object_other], background=background, connectivity=8)

    # Scale the small pattern to the big pattern
    scale_factor = np.random.randint(2, 4)
    pattern_big = scale_sprite(pattern_small, scale_factor)
    pattern_big = np.where(pattern_big == object_small, object_big, pattern_big)

    # Place the big pattern on the grid
    # The pattern can be partially outside the grid
    # Ensure the pattern is not too outside the grid
    padding = 4
    x, y = np.random.randint(padding, n - padding), np.random.randint(padding, m - padding)
    grid = blit_sprite(grid=grid, sprite=pattern_big, x=x, y=y, background=background)

    try:
        # Place the small pattern on the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=pattern_small, background=background)
        grid = blit_sprite(grid=grid, sprite=pattern_small, x=x, y=y, background=background)

        # Place the other pattern on the grid
        x, y = random_free_location_for_sprite(grid=grid, sprite=pattern_other, background=background)
        grid = blit_sprite(grid=grid, sprite=pattern_other, x=x, y=y, background=background)

        # Check if the generated grid is valid
        main(grid)
    except:
        return generate_input()

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
