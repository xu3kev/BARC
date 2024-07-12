from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, topology, logical operations

# description:
# In the input grid, you will see multiple objects (shapes) of various colors. 
# To make the output, first find the symmetrical shapes (horizontally, vertically, 
# diagonally, or radially symmetrical). Then apply a logical XOR operation on each 
# pixel between every pair of symmetrical shapes (symmetry pairs) in their respective positions. 
# The output grid colors a pixel teal if the XOR operation results in true and keeps it black otherwise.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Get the shapes
    objects = find_connected_components(input_grid, connectivity=8)
    shapes = [crop(obj) for obj in objects]
    
    # Find symmetrical shapes
    symmetrical_pairs = []
    used = set()
    for i, shape1 in enumerate(shapes):
        for j, shape2 in enumerate(shapes):
            if i >= j or j in used:
                continue
            if (np.array_equal(shape1, shape2) or
                np.array_equal(shape1, np.rot90(shape2, 1)) or
                np.array_equal(shape1, np.flipud(shape2)) or
                np.array_equal(shape1, np.fliplr(shape2)) or
                np.array_equal(shape1, shape2.T)):
                symmetrical_pairs.append((objects[i], objects[j]))
                used.add(i)
                used.add(j)
    
    # Create the output grid with XOR results
    output_grid = np.zeros_like(input_grid)
    for obj1, obj2 in symmetrical_pairs:
        for x in range(input_grid.shape[0]):
            for y in range(input_grid.shape[1]):
                if (obj1[x, y] != Color.BLACK) != (obj2[x, y] != Color.BLACK):  # XOR operation
                    output_grid[x, y] = Color.TEAL
    
    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Add symmetrical shapes
    num_shapes = np.random.randint(2, 4)
    for _ in range(num_shapes):
        symmetry = np.random.choice(['horizontal', 'vertical', 'diagonal', 'radial'])
        color = np.random.choice(Color.NOT_BLACK)
        shape = random_sprite(n=np.random.randint(2, 6), 
                              m=np.random.randint(2, 6), 
                              symmetry=symmetry, 
                              color_palette=[color])
        x, y = random_free_location_for_sprite(grid, shape)
        blit_sprite(grid, shape, x, y)
        
        # Add a symmetrical shape
        if symmetry == 'horizontal':
            shape_symmetric = np.flipud(shape)
        elif symmetry == 'vertical':
            shape_symmetric = np.fliplr(shape)
        elif symmetry == 'diagonal':
            shape_symmetric = np.transpose(shape)
        elif symmetry == 'radial':
            shape_symmetric = np.rot90(shape, 2)
        
        x, y = random_free_location_for_sprite(grid, shape_symmetric)
        blit_sprite(grid, shape_symmetric, x, y)
        
    return grid