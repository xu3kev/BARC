import os
import traceback
import sys

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'execve':
        filename = co.co_filename
        line_no = frame.f_lineno
        if 'lscpu' in str(arg):
            print(f"lscpu called from {filename}:{line_no}")
            traceback.print_stack(frame)
    return trace_calls

sys.settrace(trace_calls)

# Rest of your imports and code below this line


import json
from enum import Enum
# extract markdown code blocks
from utils import parse_code
from execution import multi_execute_transformation
from seeds.common import *
from arc import train_problems, validation_problems
import argparse
import os

from arc.read import parse_dir
def get_concept_arc_problems():
    problems = []
    for problem_directory in os.listdir("ConceptARC"):
        problems.extend(parse_dir("ConceptARC/"+problem_directory))
    
    return problems

concept_arc_problems = get_concept_arc_problems()
concept_arc_problems = list(concept_arc_problems)
# need to split problems to each test input becomes a problem
new_problems = []
from arc.types import ArcIOPair, ArcProblem
for problem in concept_arc_problems:
    for ti, test_pair in enumerate(problem.test_pairs):
        new_problem = ArcProblem(uid=f"{problem.uid}-{ti}",
                                    train_pairs=problem.train_pairs,
                                    test_pairs=[test_pair])
        new_problems.append(new_problem)
    assert len(problem.test_pairs) == 3, f"Problem {problem.uid} has {len(problem.test_pairs)} test pairs"
concept_arc_problems = new_problems

TRANSPOSE = False

MULTI_EXECUTE = True

class GridComparisonResult(Enum):
    EQUAL = 0
    SHAPE_MISMATCH = 1
    CONTENT_MISMATCH = 2
    TYPE_MISMATCH = 3
    ERROR = 4
    NON_2D_ARRAY = 5

def compare_grids(output_grid, expected_output_grid):
    if isinstance(output_grid, str):
        return GridComparisonResult.ERROR, 0.0
    
    if not isinstance(output_grid, np.ndarray):
        return GridComparisonResult.TYPE_MISMATCH, 0.0
    
    if len(output_grid.shape) != 2:
        return GridComparisonResult.NON_2D_ARRAY, 0.0
    
    if output_grid.shape != expected_output_grid.shape:
        return GridComparisonResult.SHAPE_MISMATCH, 0.0
    
    if np.array_equal(output_grid, expected_output_grid):
        return GridComparisonResult.EQUAL, 1.0
    
    # If shapes match but content doesn't, calculate the ratio of matching elements
    ratio = np.sum(output_grid == expected_output_grid) / np.prod(expected_output_grid.shape)
    return GridComparisonResult.CONTENT_MISMATCH, ratio


def validate(arc_problem, code):
    failure = False

    return_output_grids = []
    train_verdict = False
    for idx, train_pair in enumerate(arc_problem.train_pairs + arc_problem.test_pairs):
        
        if failure: break

        if idx >= len(arc_problem.train_pairs):
            train_verdict = True

        # transpose the input and output grids, because we index them x,y and they are stored as r,c

        if TRANSPOSE:
            input_grid = train_pair.x.T
            expected_output_grid = train_pair.y.T
        else:
            input_grid = train_pair.x
            expected_output_grid = train_pair.y

        try:
            output_grids = multi_execute_transformation([code], [input_grid], random_seeds=[0], timeout=2, 
                                                        function_name="transform", num_workers=32)
            output_grid = output_grids[0]
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            output_grid = "error"
            print(e)


        comparison_result, ratio = compare_grids(output_grid, expected_output_grid)
        
        if isinstance(output_grid, np.ndarray):
            return_output_grids.append(output_grid.tolist())
        else:
            return_output_grids.append(output_grid)

        return_output_grids.append(output_grid.tolist())

        if comparison_result != GridComparisonResult.EQUAL:
            failure = True
            if comparison_result == GridComparisonResult.ERROR:
                print(f"\t\t[-] Error occurred: {output_grid}")
            elif comparison_result == GridComparisonResult.TYPE_MISMATCH:
                print("\t\t[-] output is not a numpy array")
            elif comparison_result == GridComparisonResult.SHAPE_MISMATCH:
                print(f"\t\t[-] output shape does not match expected shape: {output_grid.shape} vs {expected_output_grid.shape}")
            elif comparison_result == GridComparisonResult.CONTENT_MISMATCH:
                print(f"\t\t[-] comparison failed, ratio of correct elements: {ratio}")

    if not failure: print(f"\t[+] passed")

    # if not failure and not train_verdict:
    #     print("something wrong")
    #     exit()

    return (train_verdict, not failure, return_output_grids)

def multi_validate(arc_problem, codes):

    # first execute the first input for each code to filter, leave only the correct ones
    
    results = [list() for _ in range(len(codes))]
    pairs = arc_problem.train_pairs + arc_problem.test_pairs
    for pair_idx in range(len(pairs)):
        input_grid = pairs[pair_idx].x
        try:
            output_grids = multi_execute_transformation(codes, [input_grid]*len(codes), random_seeds=[0]*len(codes),
                                                        timeout=2, function_name="transform", num_workers=64)
        except KeyboardInterrupt:
            exit()

        assert len(output_grids) == len(codes)
        
        for code_idx, output_grid in enumerate(output_grids):
            # compare
            try:
                comparison_result, ratio = compare_grids(output_grid, pairs[pair_idx].y)
            except:
                breakpoint()
            if comparison_result == GridComparisonResult.EQUAL:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            elif comparison_result == GridComparisonResult.SHAPE_MISMATCH:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            elif comparison_result == GridComparisonResult.CONTENT_MISMATCH:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            else:
                results[code_idx].append((None, 0.0))

        assert len(results) == len(codes)

    return results

def multi_validate2(arc_problem, codes):

    # do all inputs all together
    
    results = [list() for _ in range(len(codes))]
    pairs = arc_problem.train_pairs + arc_problem.test_pairs
    for pair_idx in range(len(pairs)):
        input_grid = pairs[pair_idx].x
        try:
            output_grids = multi_execute_transformation(codes, [input_grid]*len(codes), random_seeds=[0]*len(codes),
                                                        timeout=2, function_name="transform", num_workers=64)
        except KeyboardInterrupt:
            exit()

        assert len(output_grids) == len(codes)
        
        for code_idx, output_grid in enumerate(output_grids):
            # compare
            try:
                comparison_result, ratio = compare_grids(output_grid, pairs[pair_idx].y)
            except:
                breakpoint()
            if comparison_result == GridComparisonResult.EQUAL:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            elif comparison_result == GridComparisonResult.SHAPE_MISMATCH:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            elif comparison_result == GridComparisonResult.CONTENT_MISMATCH:
                results[code_idx].append((comparison_result == GridComparisonResult.EQUAL, ratio))
            else:
                results[code_idx].append((None, 0.0))

        assert len(results) == len(codes)

    return results


def get_arc_problem(uid):
    for problem in train_problems + validation_problems + concept_arc_problems:
        if problem.uid == uid:
            return problem
    assert False, f"Problem {uid} not found"
    # return None

def main():
    # answer_file = "answers_ft_gpt-4o-mini-2024-07-18_ellislab_llama2000-seeds_9qjZpfTA_train.jsonl"
    # answer_file = "answers_ft_gpt-4o-mini-2024-07-18_ellislab_llama3000-seeds_9qs7cbH2_validation.jsonl"
    # answer_file = "answers_ft_gpt-4o-mini-2024-07-18_ellislab_llama3000-seeds_9qs7cbH2_train.jsonl"
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer_file", help="Path to the answer file")
    args = parser.parse_args()
    # answer_file = "./finetune/alignment-handbook/arc_problems_train_334_responses_0816013840.jsonl"
    answer_file = args.answer_file
    with open(answer_file) as f:
        problem_answers = [json.loads(line) for line in f]

    os.makedirs("results", exist_ok=True)
    saving_file = answer_file.replace(".jsonl", "_exec_results_v4.jsonl")
    # get just the filename
    import pathlib
    saving_file = pathlib.Path(saving_file).name 
    saving_file = pathlib.Path("results") / saving_file
    print(f"Saving to {saving_file}")

    accepted = 0
    from tqdm import tqdm

    for problem_idx, p in enumerate(tqdm(problem_answers)):
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
        train_verdicts = []
        train_test_verdicts = []
        verdicts_per_example_per_sample = []
        all_output_grids = []

        # SINGLE THREAD
        if MULTI_EXECUTE == False:
            for i, code in enumerate(codes):
                # print(f"Code {i}: {code}")
                train_verdict = False
                train_test_verdict = False
                try:
                    train_verdict, train_test_verdict, output_grids = validate(arc_problem, code)
                except KeyboardInterrupt:
                    exit()
                except Exception as e:
                    train_verdict = False
                    train_test_verdict = False

                train_verdicts.append(train_verdict)
                train_test_verdicts.append(train_test_verdict)
                all_output_grids.append(output_grids)
        else:
            results = multi_validate(arc_problem, codes)
            for idx, result in enumerate(results):
                assert len(result) == len(arc_problem.train_pairs + arc_problem.test_pairs)
                train_verdict = all([verdict for verdict, _ in result[:len(arc_problem.train_pairs)]])
                train_verdicts.append(train_verdict)
                train_test_verdict = all([verdict for verdict, _ in result])
                train_test_verdicts.append(train_test_verdict)
                max_ratio = max([ratio for _, ratio in result])
                min_ratio = min([ratio for _, ratio in result])
                icon = "[+]" if train_verdict else "[ ]"
                print(f"    {icon} Code {idx}: {train_test_verdict}, max_ratio: {max_ratio}, min_ratio: {min_ratio}")
                all_output_grids.append(None)
                verdicts_per_example = [verdict for verdict, _ in result]
                verdicts_per_example_per_sample.append(verdicts_per_example)



        problem_answers[problem_idx]["train_verdicts"] = train_verdicts
        problem_answers[problem_idx]["train_test_verdicts"] = train_test_verdicts
        problem_answers[problem_idx]["output_grids"] = [] # all_output_grids
        problem_answers[problem_idx]["verdicts_per_examples"] = verdicts_per_example_per_sample
        # print(f"Train verdicts: {train_verdicts}, sum: {sum(train_verdicts)}")
        # print(f"Train test verdicts: {train_test_verdicts}, sum: {sum(train_test_verdicts)}")

        if any(train_test_verdicts):
            accepted += 1

        print(f"Accepted: {accepted}/{problem_idx+1}")

    print(f"Accepted: {accepted}/{len(problem_answers)}")
    # with open("correct_codes.json", "w") as f:
    #     f.write(json.dumps(correct_codes))
    
    print(f"Savings to {saving_file}")
    with open(saving_file, "w") as f:
        f.write("\n".join(json.dumps(p) for p in problem_answers))



if __name__ == "__main__":
    main()