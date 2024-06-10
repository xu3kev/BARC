# Code for running ARC programs

from func_timeout import func_timeout, FunctionTimedOut

import sys
# add seeds/ to the python path so we can import common
sys.path.append("seeds/")
from common import *

import numpy as np

def execute_transformation(source, input_grid, timeout=1, function_name="main"):

    global_vars = {}

    def execute_code(code, global_vars):
        exec(code, global_vars)
        return global_vars['output_grid']
            
    n, m = input_grid.shape
    make_input = f"input_grid = np.zeros(({n}, {m}), dtype=int)\n"
    for i in range(n):
        for j in range(m):
            make_input += f"input_grid[{i}][{j}] = {input_grid[i][j]}\n"
            
    code = f"""{source}
{make_input}
output_grid = {function_name}(input_grid)
"""

    try:
        output = func_timeout(timeout, execute_code, args=(code, global_vars))
    except FunctionTimedOut:
        print("Error: Code execution timed out after 10 seconds")
        output = "timeout"
    except Exception as e:
        print("Error in executing code")
        print(f"Error: {e}")
        output = f"error: {e}"

    # make sure that it is a 2d nump array of integers between 0-9
    if isinstance(output, np.ndarray) and len(output.shape) == 2 and np.all((0 <= output) & (output <= 9)):
        return output
    else:
        return "error: output is not a valid grid"

    return output

def execute_input_generator(source, timeout=1, function_name="generate_input"):

    global_vars = {}

    def execute_code(code, global_vars):
        exec(code, global_vars)
        return global_vars['grid']

    code = f"""{source}
grid = {function_name}()
"""

    try:
        output = func_timeout(timeout, execute_code, args=(code, global_vars))
    except FunctionTimedOut:
        print(f"Error: Code execution timed out after {timeout} seconds")
        output = "timeout"
    except Exception as e:
        print("Error in executing code")
        print(f"Error: {e}")
        output = f"error: {e}"

    return output