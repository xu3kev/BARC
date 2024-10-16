import sys
import os
from arc import train_problems, validation_problems
from conceptarc import concept_arc_problems
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def plot_arc_input_outputs(input_outputs, column_headings=None):
    column_headings = column_headings or ["input", "output"]
    n_pairs = len(input_outputs)
    figure, axs = plt.subplots(n_pairs, len(input_outputs[0]), figsize=(5 * len(input_outputs[0]), 5 * n_pairs))    

    # RGB
    colors_rgb = {
        0: (0x00, 0x00, 0x00),
        1: (0x00, 0x74, 0xD9),
        2: (0xFF, 0x41, 0x36),
        3: (0x2E, 0xCC, 0x40),
        4: (0xFF, 0xDC, 0x00),
        5: (0xA0, 0xA0, 0xA0),
        6: (0xF0, 0x12, 0xBE),
        7: (0xFF, 0x85, 0x1B),
        8: (0x7F, 0xDB, 0xFF),
        9: (0x87, 0x0C, 0x25),
        10: (0xFF, 0xFF, 0xFF)
    }

    _float_colors = [tuple(c / 255 for c in col) for col in colors_rgb.values()]
    arc_cmap = ListedColormap(_float_colors)

    for ex, input_output in enumerate(input_outputs):
        for col, grid in enumerate(input_output):
            ax = axs[ex,col]
            if isinstance(grid, tuple) and len(grid) == 2 and isinstance(grid[0], np.ndarray):
                grid, mask = grid
                grid = grid.copy()
                if isinstance(mask, np.ndarray):
                    grid[~mask] = 10
                else:
                    grid[grid==mask] = 10
                extra_title = " partial output"
            elif isinstance(grid, np.ndarray):
                extra_title = ""
            else:
                continue
            grid = grid.T
    
            ax.pcolormesh(
                grid,
                cmap=arc_cmap,
                rasterized=True,
                vmin=0,
                vmax=10,
            )
            ax.set_xticks(np.arange(0, grid.shape[1], 1))
            ax.set_yticks(np.arange(0, grid.shape[0], 1))
            ax.grid()
            ax.set_aspect(1)
            ax.invert_yaxis()

            if col<len(column_headings):
                ax.set_title(column_headings[col]+extra_title)
            else:
                ax.set_title(extra_title)
    plt.show()


if __name__ == '__main__':
    assert len(sys.argv) == 2, "Usage: python view_problem.py <problem_id>"

    # add seeds/ to the python path so we can import common
    sys.path.append("seeds/")

    from common import show_colored_grid

    problem_id = sys.argv[1]

    problem = [p for p in train_problems+validation_problems+concept_arc_problems() if p.uid == problem_id]
    assert len(problem) == 1, f"Problem {problem_id} not found"

    n_pairs = len(problem[0].train_pairs) + len(problem[0].test_pairs)
    figure, axs = plt.subplots(n_pairs, 2, figsize=(5, 5 * n_pairs))

    for i, pair in enumerate(problem[0].train_pairs):
        print("Input:")
        show_colored_grid(pair.x.T)
        print("Output:")
        show_colored_grid(pair.y.T)
        print("\n\n")

        pair.plot(show=False, title=problem_id, fig_axes = (figure, axs[i,:]))

    for i, pair in enumerate(problem[0].test_pairs):
        print("Test Input:")
        show_colored_grid(pair.x.T)
        print("Test Output:")
        show_colored_grid(pair.y.T)
        print("\n\n")

        pair.plot(show=False, title=problem_id, fig_axes = (figure, axs[i + len(problem[0].train_pairs),:]))

    plt.show()
