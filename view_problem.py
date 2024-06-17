import sys
import os
from arc import train_problems
import matplotlib.pyplot as plt

assert len(sys.argv) == 2, "Usage: python view_problem.py <problem_id>"

# add seeds/ to the python path so we can import common
sys.path.append("seeds/")

from common import show_colored_grid

problem_id = sys.argv[1]

problem = [p for p in train_problems if p.uid == problem_id]
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
