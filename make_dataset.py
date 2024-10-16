from arc import train_problems, validation_problems
import os
import re
from prompt import get_common_lib_from_file
import json
import numpy as np
import tiktoken


class IOPair:
    x: np.ndarray
    y: np.ndarray
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # check type
        assert isinstance(self.x, np.ndarray)
        assert isinstance(self.y, np.ndarray)
        # check shape
        assert len(self.x.shape) == 2
        assert len(self.y.shape) == 2

class Problem:
    # typing hint for the members
    filename: str
    seed_id: str
    code: str
    train_pairs: list
    test_pairs: list

    def __init__(self, filename=None, code=None, seed_id=None, train_pairs=None, test_pairs=None):
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
            self.load_arc_problem(self.seed_id)

        self.code = code
        if train_pairs:
            self.train_pairs = train_pairs
        if test_pairs:
            self.test_pairs = test_pairs

        assert self.code, "Code is not provided"
        assert self.train_pairs, "Train pairs are not provided"
        assert self.test_pairs, "Test pairs are not provided"
        # check type
        assert isinstance(self.train_pairs, list)
        assert isinstance(self.test_pairs, list)
        assert all(isinstance(pair, IOPair) for pair in self.train_pairs)
        assert all(isinstance(pair, IOPair) for pair in self.test_pairs)


    def load_arc_problem(self, seed_id):
        # using train_problems
        arc_problem = None
        for problem in train_problems + validation_problems:
            if problem.uid == seed_id:
                arc_problem = problem
                break
        assert arc_problem is not None
        self.train_pairs = []
        for pair in arc_problem.train_pairs:
            self.train_pairs.append(IOPair(pair.x.T, pair.y.T))
        self.test_pairs = []
        for pair in arc_problem.test_pairs:
            self.test_pairs.append(IOPair(pair.x.T, pair.y.T))

def grid_to_input(grid):
    return "\n".join("|".join(str(c) for c in row) for row in grid)

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

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_seeds", action="store_true")
    parser.add_argument("--load_file", type=str)

    args = parser.parse_args()

    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    seeds = [seed for seed in seeds if re.match(pattern, seed)]


    common_lib, _ = get_common_lib_from_file("seeds/common.py")

    seed_problems = []
    if args.use_seeds:
        for seed in seeds:
            with open(f"seeds/{seed}") as f:
                content = f.read()
                assert "# ============= remove below this point for prompting =============" in content
                content = content.split("# ============= remove below this point for prompting =============")[0].strip()
                content = content.split("def generate_input")[0].strip()
                content = content.replace("def main(", "def transform(")
                seed_problems.append(Problem(filename=seed, code=content))

    print(f"got {len(seed_problems)} seed problems")


    loaded_problems = []
    if args.load_file:
        assert args.load_file.endswith(".jsonl"), "Expected a jsonl file"
        assert os.path.exists(args.load_file), "File does not exist"
        loaded_data = []
        with open(args.load_file) as f:
            for line in f:
                loaded_data.append(json.loads(line))
                

        for d in loaded_data:
            all_pairs = []
            for example in d["examples"]:
                input_grid = np.array(example[0])
                output_grid = np.array(example[1])
                all_pairs.append(IOPair(input_grid, output_grid))

            code = d['source']
            if "def generate_input" not in code or "def main(" not in code:
                continue
            code = code.split("def generate_input")[0].strip()
            code = code.replace("def main(", "def transform(")
            # use first 3 pairs as train pairs and 4th pair as test pair
        
            problem = Problem(code=code, train_pairs=all_pairs[0:3], test_pairs=[all_pairs[3]])

            loaded_problems.append(problem)

    print(f"get {len(loaded_problems)} problems from file")
        

    train_data = []
    # random shuffle with seed 0
    import random
    random.seed(0)

    if loaded_problems:
        random.shuffle(loaded_problems)
    loaded_problems = loaded_problems[0:3000]

    problems = loaded_problems + seed_problems
    for problem in problems:
        question = make_input_prompt(problem, common_lib)
        answer = f"""Let's solve this puzzle using Python code with the common library functions. We first reasoning about the problem and then writing the code to solve it. The `transform` function will take the input grid and return the output grid. Here is the Python code and the comments describing how to solve the problem:
```python
{problem.code}
```
""" 
        train_data.append(convert_chat_format(question, answer))

    print("==============input=============")
    print(train_data[0]["messages"][1]["content"])
    print("==============output=============")
    print(train_data[0]["messages"][2]["content"])


    # calculate total number of tokens
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    token_count = 0
    for data in train_data:
        token_count += len(encoding.encode(data["messages"][0]["content"]))
        token_count += len(encoding.encode(data["messages"][1]["content"]))
        token_count += len(encoding.encode(data["messages"][2]["content"]))
    
    print(f"Total number of tokens: {token_count}")
    print(f"Averge number of tokens per example: {token_count / len(train_data)}")

    with open("openai_ft_data.jsonl", "w") as f:
        f.write("\n".join(json.dumps(data) for data in train_data))

if __name__ == "__main__":
    main()