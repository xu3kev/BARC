from llm import *
from prompt import get_common_lib_from_file
from execution import multi_execute_transformation, multi_execute_input_generator, execute_transformation
from utils import extract_functions
from view_problem import plot_arc_input_outputs
from arc import train_problems
import numpy as np

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "problem generator")
    
    parser.add_argument("--batch_size", "-b", type=int, default=1, help="how many samples to draw")
    parser.add_argument("--temperature", "-t", type=float, default=0.0)
    parser.add_argument("--model", "-m", type=str, default="gpt-4-turbo", help="which model to use", 
                        choices=[m.value for model_list in LLMClient.AVAILABLE_MODELS.values() for m in model_list])
    parser.add_argument("--max_tokens", type=int, default=2048, help="max number of tokens for generation")
    parser.add_argument("--visualize", "-v", action="store_true", help="visualize the refactoring")
    parser.add_argument("problem", type=str, help="which problem to refactor")
    
    arguments = parser.parse_args()

    # convert model into enum
    possible_provider_models = [(provider, model) for provider, model_list in LLMClient.AVAILABLE_MODELS.items() for model in model_list if model.value == arguments.model]
    assert len(possible_provider_models)>0, f"Model {arguments.model} not found"
    for provider, model in possible_provider_models:
        try:
            client = LLMClient(provider=provider)
            print(f"Using model {model.value} from provider {provider.name}")
        except Exception as e:
            print(f"{provider}/{model.value} not available: {e}")

    assert any( problem.uid == arguments.problem for problem in train_problems), "unknown problem"
    problem = [problem for problem in train_problems if problem.uid == arguments.problem][0]
    input_grids = [train_pair.x for train_pair in problem.train_pairs]
    input_grids += [train_pair.x for train_pair in problem.test_pairs]
    input_grids = [input_grid.T for input_grid in input_grids]
    target_outputs = [train_pair.y.T for train_pair in problem.train_pairs] + [train_pair.y.T for train_pair in problem.test_pairs]


    seed = arguments.problem
    with open(f"seeds/{seed}.py") as f:
        content = f.read()
        assert "\ndef generate_input" in content
        content = content.split("\ndef generate_input")[0].strip()
        seed = content
    
    common_lib, common_lib_function_names = get_common_lib_from_file("seeds/common.py", reference_code=seed)

    # read the prompt template from prompts/divide_and_conquer_refactor.md
    with open("prompts/divide_and_conquer_refactor.md") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(original=seed, common=common_lib)
    print(prompt)
    
    generations = client.generate(prompt, num_samples=arguments.batch_size, max_tokens=arguments.max_tokens, temperature=arguments.temperature, model=model)

    for i, generation in enumerate(generations):
        print(f"Refactored problem {i+1}:\n{generation}")
        print("=====================================================")
        print()

        # extract code block
        code_block = generation.split("```python")[1].split("```")[0].strip()
        code_block = "from typing import Tuple, List\nimport numpy as np\nfrom common import *\n"+code_block
        try:
            functions = list(set([f["name"] for f in extract_functions(code_block)]))
        except:
            print("Error extracting functions, almost certainly a syntax error in the generated code")
            continue
        functions.sort(key=lambda x: (x!="main", x))
        print(functions)
        

        # now we run each function on each input

        # Theoretically these are self contained functions, so we can just run them on the input grid
        arc_array = [ [input_grid] + [ execute_transformation(code_block, input_grid, function_name=fn) for fn in functions] for input_grid in input_grids]

        predicted_outputs = [ r[1] for r in arc_array]
        all_predicted_correctly = all( np.array_equal(predicted_output, expected_output) for predicted_output, expected_output in zip(predicted_outputs, target_outputs))
        def legal_intermediate(intermediate):
            return isinstance(intermediate, tuple) and len(intermediate) == 2 and isinstance(intermediate[0], np.ndarray) and \
                (intermediate[1] is None or isinstance(intermediate[1], int)) and\
                 np.all((0 <= intermediate[0]) & (intermediate[0] <= 9))
        all_intermediate_legal = all( all( legal_intermediate(output) for output in row[2:])
                                     for row in arc_array)
        
        print("Legal refactoring:", all_intermediate_legal)
        print("Correct refactoring:", all_predicted_correctly)
        print("Totally Correct:", all_intermediate_legal and all_predicted_correctly)

        if arguments.visualize: plot_arc_input_outputs(arc_array, column_headings=["input"]+functions)

