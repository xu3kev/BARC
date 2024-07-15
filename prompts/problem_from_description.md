You are a puzzle maker designing geometric, physical, and topological puzzles for curious middle-schoolers.

Each puzzle consists of discovery a deterministic rule, pattern, procedure, algorithm, or transformation law that maps inputs to outputs.
Both the inputs and outputs are 2D grids of colored pixels. There are 10 colors, but the order of the colors is never relevant to the puzzle.

The middle schoolers are trying to discover this deterministic transformation, which can be implemented as a Python function called `main`.
Designing a puzzle involves also creating example inputs, which can be implemented as a Python function called `generate_input`. Unlike `main`, the `generate_input` function should be stochastic, so that every time you run it, you get another good example of what the transformation can be applied to.

Here is a overview of the puzzle you will design:

{description}

Please design the puzzle by writing code containing the `generate_input` and `main` functions. You can use the following standard library (`common.py`):

```python
{common_lib}
```

To give you ideas on how to implement the puzzle, here are some examples of other puzzles with similar descriptions:

{examples}

Your task is to create a new puzzle that matches the description above and is implemented similar to the example puzzles, following these steps:

1. Inspect the example puzzle implementations, making note of the functions used and the physical/geometric/topological/logical details
2. Brainstorm a possible implementation for the new puzzle's description
3. Generate a code block formatted like the earlier examples with a comment starting `# concepts:` listing the concepts and `# description:` describing the inputs and transformation from the given description.

Be sure to make the transformation `main` deterministic. Be sure to not assume or impose any ordering to the colors. Use physical, geometric, topological, and logical concepts.
