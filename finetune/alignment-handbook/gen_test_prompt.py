import os
import tqdm
import json
from gen_dataset import Problem, make_input_prompt, convert_chat_format
from arc import validation_problems, train_problems
from arc.types import ArcIOPair, ArcProblem
import re

from gen_dataset import TRANSPOSE, EXTRA_NEWLINE

from arc.read import parse_dir
import os

def get_concept_arc_problems():
    problems = []
    for problem_directory in os.listdir("../../ConceptARC"):
        problems.extend(parse_dir("../../ConceptARC/"+problem_directory))
    
    return problems


concept_arc_problems = get_concept_arc_problems()
# assert every uid is unique
uids = [p.uid for p in concept_arc_problems]
assert len(uids) == len(set(uids))

# SPLIT="validation"
# SPLIT = "train"
SPLIT = "concept_arc"

# SPLIT = "selected-val-subset50.json"
# SPLIT = "selected-train-subset50.json"

VERSION = "v2"

ALL_PROBLEMS = []

def main():

    # get problems under the seed directory
    seeds = os.listdir("../../seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"[0-9a-f]{8}(_[a-zA-Z]+)?\.py"
    # get all files and its content
    seeds = [seed for seed in seeds if re.match(pattern, seed)]
    def extract_uid(seed):
        uid = ""
        if "." in seed:
            uid = seed.split(".")[0]
        if "_" in uid:
            uid = uid.split("_")[0]
        return uid
    seeds_uid = [extract_uid(seed) for seed in seeds]
    print(len(seeds))
    print(seeds_uid)


    import random
    random.seed(0)
    if SPLIT == "train":
        problems = list(train_problems)
        random.shuffle(problems)
    elif SPLIT == "validation":
        problems = list(validation_problems)
        random.shuffle(problems)
    elif SPLIT == "concept_arc":
        problems = list(concept_arc_problems)
        # need to split problems to each test input becomes a problem
        new_problems = []
        for problem in problems:
            for ti, test_pair in enumerate(problem.test_pairs):
                new_problem = ArcProblem(uid=f"{problem.uid}-{ti}",
                                         train_pairs=problem.train_pairs,
                                         test_pairs=[test_pair])
                new_problems.append(new_problem)
            assert len(problem.test_pairs) == 3, f"Problem {problem.uid} has {len(problem.test_pairs)} test pairs"
        problems = new_problems
            
    elif SPLIT.endswith(".json"):
        # load the json file
        problems = []
        with open(SPLIT) as f:
            loaded_problem_data = json.loads(f.read())

        uids = [p['name'].split(".json")[0] for p in loaded_problem_data]
        for uid in uids:
            for arc_problem in train_problems + validation_problems:
                if arc_problem.uid == uid:
                    problems.append(arc_problem)
    else:
        raise ValueError(f"Invalid SPLIT value: {SPLIT}")

    # save all problems

    seed_uid_hit = []
    for arc_problem in tqdm.tqdm(problems):
        
        uid = arc_problem.uid
        if uid in seeds_uid:
            seed_uid_hit.append(uid)
            continue
        if SPLIT == "concept_arc":
            problem = Problem(arc_problem=arc_problem, code="# No code")
        else:
            problem = Problem(seed_id=arc_problem.uid, code="# No code")

        question = make_input_prompt(problem, transpose=True)
    
#         answer = f"""Let's solve this puzzle using Python code with the common library functions. We'll first reason about the problem and then write the code to solve it. The `transform` function will take the input grid and return the output grid. Here is the Python code with the comments describing how to solve the problem:
# ```python
# """
        messages = convert_chat_format(question, None)['messages']
        ALL_PROBLEMS.append({"uid": uid, "messages": messages})

    breakpoint()
        

    # print([p['uid'] for p in ALL_PROBLEMS[0:50]])
    # print(f"The number of problems is {len(ALL_PROBLEMS)}")

    # breakpoint()
    
    if ".json" in SPLIT:
        split_filename = SPLIT.split(".json")[0]
    else:
        split_filename = SPLIT
    problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}.jsonl"
    if TRANSPOSE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_transpose.jsonl"
    if EXTRA_NEWLINE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_extra_newline.jsonl"
    if TRANSPOSE and EXTRA_NEWLINE:
        problem_file = f"arc_problems_{split_filename}_{len(ALL_PROBLEMS)}_transpose_extra_newline.jsonl"

    if VERSION:
        problem_file = problem_file.replace(".jsonl", f"_{VERSION}.jsonl")
    
    print(f"Saving to {problem_file}")
    with open(problem_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in ALL_PROBLEMS))

    # with open(saving_file, "w") as f:
    #     f.write("\n".join(json.dumps(p) for p in all_problem_answers))

if __name__ == "__main__":
    main()
