import json
# extract markdown code blocks
from utils import parse_code
from execution import execute_transformation
from seeds.common import *
from arc import train_problems, validation_problems

def validate(arc_problem, code):
    failure = False

    for train_pair in arc_problem.train_pairs + arc_problem.test_pairs:
        if failure: break
        # transpose the input and output grids, because we index them x,y and they are stored as r,c
        input_grid = train_pair.x.T
        expected_output_grid = train_pair.y.T

        try:
            output_grid = execute_transformation(code, input_grid, timeout=2, function_name="transform")
        except:
            output_grid = "error"

        if isinstance(output_grid, str):
            failure = True
            continue

        if not np.array_equal(output_grid, expected_output_grid):
            failure = True

    if not failure: print(f"\t[+] passed")

    return not failure

def get_arc_problem(uid):
    for problem in train_problems + validation_problems:
        if problem.uid == uid:
            return problem
    return None

def main():
    with open("answers.jsonl") as f:
        problem_answers = [json.loads(line) for line in f]

    accepted = 0
    for p in problem_answers:
        uid = p["uid"]
        responses = p["responses"]
        print(f"Problem: {uid}")
        codes = []
        for i, response in enumerate(responses):
            parsed_codes = parse_code(response)
            if parsed_codes:
                code = parsed_codes[0]
            else:
                code = ""
            codes.append(code)

        arc_problem = get_arc_problem(uid)
        pass_or_not = False
        for i, code in enumerate(codes):
            print(f"Code {i}: {code}")
            if validate(arc_problem, code):
                pass_or_not = True

        if pass_or_not:
            accepted += 1

    print(f"Accepted: {accepted}/{len(problem_answers)}")



if __name__ == "__main__":
    main()