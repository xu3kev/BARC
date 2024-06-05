import sys
import os
from arc import train_problems
import matplotlib.pyplot as plt

assert len(sys.argv) == 2, "Usage: python view_problem.py <problem_id>"

# copy common.py from seeds to the current directory and then do the import
# this is a hack
os.system("cp seeds/common.py .")

from common import show_colored_grid

problem_id = sys.argv[1]

problem = [p for p in train_problems if p.uid == problem_id]
assert len(problem) == 1, f"Problem {problem_id} not found"

n_pairs = len(problem[0].train_pairs) + len(problem[0].test_pairs)
figure, axs = plt.subplots(n_pairs, 2, figsize=(5, 5 * n_pairs))

for i, pair in enumerate(problem[0].train_pairs):
    print("Input:")
    show_colored_grid(pair.x)
    print("Output:")
    show_colored_grid(pair.y)
    print("\n\n")

    pair.plot(show=False, title=problem_id, fig_axes = (figure, axs[i,:]))

for i, pair in enumerate(problem[0].test_pairs):
    print("Test Input:")
    show_colored_grid(pair.x)
    print("Test Output:")
    show_colored_grid(pair.y)
    print("\n\n")

    pair.plot(show=False, title=problem_id, fig_axes = (figure, axs[i + len(problem[0].train_pairs),:]))

plt.show()

# cleanup
os.system("rm common.py")