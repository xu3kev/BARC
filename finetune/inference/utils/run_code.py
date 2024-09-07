import sys
import os
import signal as signal_

timeout = 20

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Execution timed out")

signal_.signal(signal_.SIGALRM, timeout_handler)

def append_function_call(code, input_martix, logger):
    global timeout
    intput = f"input = np.array({input_martix})\n\n"
    call_function = "print(transform(input))\n"
    code += '\n\n' + intput + call_function
    os.makedirs('result', exist_ok=True)
    try:
        with open('result/arc_code_output_tempt.txt', 'w') as file:
            sys.stdout = file
            signal_.alarm(timeout)
            exec(code, globals())
            sys.stdout = sys.__stdout__
            signal_.alarm(0)
        with open('result/arc_code_output_tempt.txt', 'r') as file:
            output = file.read()[:-1]
    except TimeoutError:
        sys.stdout = sys.__stdout__
        output = "Excuation Error: Execution timed out"
        if logger is not None:
            logger.error("Execution timed out")
        else:
            # print("Execution timed out")
            pass
    except Exception as e:
        sys.stdout = sys.__stdout__
        # print(f"Excuation Error: {e}")
        if logger is not None:
            logger.error(f"Excuation Error: {e}")
        else:
            # print(f"Excuation Error: {e}")
            pass
        # logger.error(f"Code: {code}")
        output = "Error: " + str(e)
    return output, code

def transform_format_to_list(matrix):
    transform_success = True
    list_matrix = []
    if 'array' in matrix:
        return None, False
    # print(matrix)
    try:
        # numpy format
        list_matrix = matrix.replace('\n','')
        list_matrix = list_matrix.replace(' ',',')
        list_matrix = eval(list_matrix)
    except Exception as e:
        try:
            # list format
            list_matrix = eval(matrix)
        except Exception as e:
            # other wrong format
            transform_success = False
    return list_matrix, transform_success

def get_code_answer(train_task, code, logger):
    Correct_task = []
    Wrong_task = []
    RE_task = []
    for i, train in enumerate(train_task['train']):
        code_output, _ = append_function_call(code, train['input'], logger)
        if "Excuation Error:" in code_output:
            RE_task.append({'input': train['input'], 'correct_output': train['output'], 'code_output': f"{code_output}"})
            break
        list_code_output, success = transform_format_to_list(code_output)
        if success == False:
            RE_task.append({'input': train['input'], 'correct_output': train['output'], 'code_output': 
                               "wrong output format: " + code_output + "\n The correct format should be np.array"})
            break
        elif list_code_output == train['output']:
            Correct_task.append({"input": train['input'], "output" :[list_code_output]})
        else:
            Wrong_task.append({'input': train['input'], 'correct_output': train['output'], 'code_output': list_code_output})

    pass_train = (len(Wrong_task) == 0 ) and (len(RE_task) == 0) and (len(Correct_task) == len(train_task['train']))
    return Correct_task, Wrong_task, RE_task, pass_train

def test_code_final(train_task, code, logger):
    test_output, _ = append_function_call(code, train_task['test'][0]['input'], logger)
    list_test_output, _ = transform_format_to_list(test_output)
    pass_it = list_test_output == train_task['test'][0]['output']
    return pass_it, list_test_output
