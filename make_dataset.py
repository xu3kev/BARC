from arc import train_problems, validation_problems
from arc.types import ArcIOPair
import os
import re
from prompt import get_common_lib_from_file
import json


class Problem:
    # typing hint for the members
    filename: str
    seed_id: str
    code: str
    train_pairs: list[ArcIOPair]
    test_pairs: list[ArcIOPair]

    def __init__(self, filename=None, code=None, seed_id=None):
        self.filename = filename
        self.seed_id = None
        if filename:
            self.seed_id = filename.split(".")[0]
            if "_" in self.seed_id:
                self.seed_id= self.seed_id.split("_")[0]
        if seed_id:
            self.seed_id = seed_id
        if self.seed_id:
            pattern = r"[0-9a-f]{8}"
            assert re.match(pattern, self.seed_id)
        self.code = code
        arc_problem = self.load_arc_problem(self.seed_id)
        self.train_pairs = arc_problem.train_pairs
        self.test_pairs = arc_problem.test_pairs

    def load_arc_problem(self, seed_id):
        # using train_problems
        for problem in train_problems + validation_problems:
            if problem.uid == seed_id:
                return problem

    def __str__(self):
        return f"Problem(seed={self.seed}, content={self.content})"

    def __repr__(self):
        return self.__str__()

def grid_to_input(grid):
    return "\n".join("".join(str(c) for c in row) for row in grid)

def make_problem_input_str(problem: Problem):
    prompt = ""
    prompt += "The following is a puzzle from the ARC dataset. Given training examples of input and output grids, predict the output grid for the test inputs.\n"
    prompt += "Here are the input and output grids for the training examples:\n"
    for pair in problem.train_pairs:
        prompt += f"Input:\n{grid_to_input(pair.x)}\nOutput:\n{grid_to_input(pair.y)}\n\n" 
    prompt += "Here are the input grids for the test example:\n"
    prompt += "Input:\n" + "\n".join(grid_to_input(pair.x) for pair in problem.test_pairs)
    return prompt

    # if problem.code:
    #     prompt += "The code to transform the input grid to the output grid is given below:\n"
    #     prompt += problem.code

def make_input_prompt(problem: Problem, common_lib: str):
    common_lib_prefix = f"""
We first define a common library that contains the functions that you can use to solve the Puzzle.
Here is the common library function signature and docstring that you can use to solve the problem (skipping the implementation for brevity):
```python
{common_lib}
```
"""
    question = common_lib_prefix + make_problem_input_str(problem)
    return question

DEFAULT_SYSTEM_PROMPT = "You are an world-class puzzle solver who are extremely good at spotting patterns and solving puzzles. You are also an expert Python programmer who can write code to solve puzzles."

def convert_chat_format(question, answer):
    messages =  {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
    }
    if answer:
        messages["messages"].append({"role": "assistant", "content": answer})
    return messages

def main():
    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]

    seed_contents = []

    problems = []

    common_lib, common_lib_function_names = get_common_lib_from_file("seeds/common.py")
    for seed in seeds:
        with open(f"seeds/{seed}") as f:
            content = f.read()
            assert "# ============= remove below this point for prompting =============" in content
            content = content.split("# ============= remove below this point for prompting =============")[0].strip()
            content = content.split("def generate_input")[0].strip()
            content = content.replace("def main(", "def transform(")
            problems.append(Problem(filename=seed, code=content))

    train_data = []
    for problem in problems:
        question = make_input_prompt(problem, common_lib)
        answer = f"""Let's solve this puzzle using Python code with the common library functions. We first reasoning about the problem and then writing the code to solve it. The `transform` function will take the input grid and return the output grid. Here is the Python code and the comments describing how to solve the problem:
```python
{problem.code}
```
""" 
        train_data.append(convert_chat_format(question, answer))
    # print("==============input=============")
    # print(train_data[0]["messages"][1]["content"])
    # print("==============output=============")
    # print(train_data[0]["messages"][2]["content"])

    with open("golden_seeds_train_data.jsonl", "w") as f:
        f.write("\n".join(json.dumps(data) for data in train_data))

if __name__ == "__main__":
    main()