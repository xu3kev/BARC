from common import *

import numpy as np

# concepts:
# objects, topology, object merging

# description:
# In the input grid, you will see various colored objects. Some objects are overlapping with each other, while others are separate.
# To create the output grid, merge overlapping objects into a single object with a unique color.

def main(input_grid):
    output_grid = input_grid.copy()

    # Find all connected components (objects) in the input grid, using 8-way connectivity
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # Create a list to keep track of which objects have been merged
    has_merged = [False] * len(objects)
    
    color_counter = len(Color.NOT_BLACK) + 1  # Start assigning new colors from here
    
    for i, obj1 in enumerate(objects):
        if has_merged[i]:
            continue

        for j, obj2 in enumerate(objects):
            if i >= j or has_merged[j]:
                continue

            # Check if obj1 and obj2 overlap
            if contact(object1=obj1, object2=obj2):
                # Merge obj2 into obj1 and mark obj2 as merged
                merged_object = obj1 | obj2
                
                # Assign a unique color to the merged object
                merged_object[merged_object != Color.BLACK] = color_counter
                color_counter += 1

                # Update obj1 to be the merged object
                objects[i] = merged_object

                # Mark obj2 as merged
                has_merged[j] = True

        # Blit the merged object back to the output grid
        object_bbox = bounding_box(objects[i])
        blit(output_grid, objects[i], x=object_bbox[0], y=object_bbox[1], background=Color.BLACK)

    return output_grid

def generate_input():
    # Make a black grid of random size
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    num_objects = np.random.randint(3, 7)

    for _ in range(num_objects):
        obj = random_sprite(n=3, m=3, density=0.5, symmetry=None, color_palette=[Color.RED, Color.GREEN, Color.BLUE])
        try:
            x, y = random_free_location_for_object(grid, obj)
            blit(grid, obj, x, y)
        except ValueError:
            break  # No more space to place new objects

    return grid