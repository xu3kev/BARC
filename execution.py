# Code for running ARC programs

from func_timeout import func_timeout, FunctionTimedOut
import concurrent.futures
import os
import signal
import sys
import psutil
import time


# add seeds/ to the python path so we can import common
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{CURRENT_DIR}/seeds/")

import numpy as np
import random

def _worker(task_id, source_code, return_var_name):
    global_vars = {}
    exec(source_code, global_vars)
    if return_var_name not in global_vars:
        print(f"Error: {return_var_name} not found in global_vars")
        return None
    ret = global_vars[return_var_name]
    return ret

def kill_process(pid):
    """Attempt to terminate the process gracefully, then forcefully if needed."""
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)  # Give some time for graceful termination
        if psutil.pid_exists(pid):
            os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # Process is already terminated
    except Exception as e:
        print(f"Error while trying to terminate the process: {e}")

def terminate_all_processes():
    """Terminate all child processes of the current process."""
    current_process = psutil.Process()
    for child in current_process.children(recursive=True):
        kill_process(child.pid)

def _worker_with_id(args):
    task_id, source_code, return_var_name = args
    # global_vars = {}
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in ['os', 'sys']:
            raise ImportError(f"Import of '{name}' is not allowed")
        return __import__(name, globals, locals, fromlist, level)

    safe_builtins = {
        k: v for k, v in __builtins__.items()
        if k not in ['exit', 'quit']
    }
    safe_builtins['__import__'] = safe_import

    safe_globals = {
        '__builtins__': safe_builtins,
    }
    exec(source_code, safe_globals)
    if return_var_name not in safe_globals:
        print(f"Error: {return_var_name} not found in global_vars")
        return None
    ret = safe_globals[return_var_name]
    return task_id, ret

def multi_process_execute(codes, return_var_name, timeout=1, num_workers=8):
    from pebble import ProcessPool, ProcessExpired

    tasks = [(i, code, return_var_name) for i, code in enumerate(codes)]
    ordered_results = [None] * len(tasks)
    with ProcessPool(max_workers=num_workers) as pool:
        future = pool.map(_worker_with_id, tasks, timeout=timeout)

        iterator = future.result()

        while True:
            try:
                result = next(iterator)
                if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], int):
                    task_id, value = result
                    ordered_results[task_id] = value
            except StopIteration:
                break
            except TimeoutError as error:
                print("function took longer than %d seconds" % timeout)
            except ProcessExpired as error:
                print("%s. Exit code: %d" % (error, error.exitcode))
            except Exception as error:
                print("function raised %s" % error)
                # print(error.traceback)  # Python's traceback of remote process
    return ordered_results

def multi_process_execute_v2(codes, return_var_name, timeout=1, num_workers=8):
    # associate each code with an index
    tasks = [(i, code, return_var_name) for i, code in enumerate(codes)]
    all_results = [None] * len(tasks)
    with concurrent.futures.ProcessPoolExecutor(num_workers) as executor:
        future_to_task = {executor.submit(_worker, task[0], *task[1:]): task for task in tasks}

        try:
            completed_futures = concurrent.futures.wait(future_to_task.keys(), timeout=timeout, return_when=concurrent.futures.ALL_COMPLETED)
            
            # Process completed futures
            for future in completed_futures.done:
                task = future_to_task[future]
                try:
                    result = future.result()  # Non-blocking result fetch
                    all_results[task[0]] = result
                except concurrent.futures.TimeoutError:
                    print(f"Task {task[0]} timed out")
                except Exception as e:
                    print(f"Task {task[0]} generated an exception: {e}")

            # Cancel remaining futures
            for future in completed_futures.not_done:
                future.cancel()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            terminate_all_processes()

        return all_results


def execute_transformation(source, input_grid, timeout=1, function_name="main"):

    input_grid = np.array(input_grid)

    global_vars = {}

    def execute_code(code, global_vars):
        exec(code, global_vars)
        return global_vars['output_grid']
            
    n, m = input_grid.shape
    make_input = f"input_grid = np.zeros(({n}, {m}), dtype=int)\n"
    for i in range(n):
        for j in range(m):
            make_input += f"input_grid[{i}][{j}] = {input_grid[i][j]}\n"
            
    code = f"""import numpy as np
from common import *
{source}
{make_input}
output_grid = {function_name}(input_grid)
"""

    try:
        if timeout is None:
            output = execute_code(code, global_vars)
        else:
            output = func_timeout(timeout, execute_code, args=(code, global_vars))
    except FunctionTimedOut:
        print("Error: Code execution timed out after 10 seconds")
        output = "timeout"
    except Exception as e:
        import traceback
        print("Error in executing code")
        print(f"Traceback: {traceback.format_exc()}")
        output = f"error: {e}"

    # make sure that it is a 2d nump array of integers between 0-9
    # if output_validator is None:
    #     output_validator = lambda out: isinstance(out, np.ndarray) and len(out.shape) == 2 and np.all((0 <= out) & (out <= 9))
    
    # if output_validator(output):
    #     return output

    return output

with open("seeds/common.py", "r") as f:
    COMMON_LIBRARY_CODE = f.read()

def multi_execute_transformation(sources, input_grids, random_seeds, timeout=1, function_name="main", num_workers=8):

    input_grids = [np.array(input_grid) for input_grid in input_grids]
            
    codes = []
    for source, input_grid, seed in zip(sources, input_grids, random_seeds):
        try:
            n, m = input_grid.shape
        except:
            breakpoint()
        make_input = f"input_grid = np.zeros(({n}, {m}), dtype=int)\n"
        for i in range(n):
            for j in range(m):
                make_input += f"input_grid[{i}][{j}] = {input_grid[i][j]}\n"
                
        code = f"""
{COMMON_LIBRARY_CODE}        
import numpy as np
import random as random98762
random98762.seed({seed})
np.random.seed({seed})
{source}
{make_input}
output_grid = {function_name}(input_grid) 
"""
        codes.append(code)

    outputs = multi_process_execute(codes, "output_grid", timeout=timeout, num_workers=num_workers)

    # make sure that it is a 2d nump array of integers between 0-9
    for idx, output in enumerate(outputs):
        try:
            if isinstance(output, np.ndarray) and len(output.shape) == 2 and np.all((0 <= output) & (output <= 9)):
                outputs[idx] = output
            else:
                outputs[idx] = "error"
        except:
            outputs[idx] = "error"

    return outputs

def execute_input_generator(source, timeout=1, function_name="generate_input"):

    global_vars = {}

    def execute_code(code, global_vars):
        exec(code, global_vars)
        return global_vars['grid']

    code = f"""import random
import numpy as np
from common import *
{source}
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

def multi_execute_input_generator(sources, random_seeds, timeout=1, function_name="generate_input", num_workers=8):

    codes = [f"""import random
import numpy as np
random.seed({random_seed})
np.random.seed({random_seed})
from common import *
{source}
grid = {function_name}()
""" for source, random_seed in zip(sources, random_seeds)]


    outputs = multi_process_execute(codes, "grid", timeout=timeout, num_workers=num_workers)

    return outputs