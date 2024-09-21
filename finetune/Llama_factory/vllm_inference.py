from utils.llm import LLMClient, Provider,VLLMModels
import json
from utils.run_code import get_code_answer
import argparse
from utils.vllm_setup import start_model_server

parser = argparse.ArgumentParser()
parser.add_argument('--train_or_evaluate', type=str, default='evaluate', help='train or evaluate')
parser.add_argument('--evaluation_test_all', type=bool, default=True)
parser.add_argument('--cache_dir', type=str, default='cache/llama31_8B_transduction/')
parser.add_argument('--model_name', type=str, default='models/llama31_8B_transduction')
args = parser.parse_args()

if_transduction = False
if_induction = True
if_transduction_and_induction = if_transduction and if_induction

for arg in vars(args):
    print(arg, getattr(args, arg))

process, available_port, base_url = start_model_server()

if args.train_or_evaluate == 'evaluate' and args.evaluation_test_all:
    format_testdir = '../get_test_dataset/arc_all_evaluation_string.json'
    original_testdir = '../get_test_dataset/original_dataset/arc_all_evaluation.json'
    transduction_dir = '../get_test_dataset/arc_all_evaluation_direct_string.json'
elif args.train_or_evaluate == 'evaluate' and not args.evaluation_test_all:
    format_testdir = '../get_test_dataset/arc_test_50_wending_string_evaluation.json'
    original_testdir = '../get_test_dataset/arc_test_50_evaluation.json'
    transduction_dir = '../get_test_dataset/arc_test_50_direct_string_evaluation.json'
elif args.train_or_evaluate == 'train':
    format_testdir = '../get_test_dataset/arc_test_50_wending_string.json'
    original_testdir = '../get_test_dataset/arc_test_50.json'
    transduction_dir = '../get_test_dataset/arc_test_50_direct_string.json'

with open(format_testdir , 'r') as f:
    data = json.load(f)

with open(transduction_dir, 'r') as f:
    transduction_data = json.load(f)


if if_transduction_and_induction:
    system_content = data[0]['messages'][0]['content']
else:
    system_content = data[0]['messages'][0]['content'].replace('[Do induction and generate executable code for output]\n', '')

llm = LLMClient(provider=Provider.VLLM, system_content=data[0]['messages'][0]['content'], cache_dir=args.cache_dir, base_url=base_url)

with open(original_testdir, 'r') as f:
    test_pur_dataset = json.load(f)
    
pass_task_name = []
cnt_zero_output = 0
for cnt, d in enumerate(data):
    if_pass = False
    print(cnt)
    print('pass', len(pass_task_name))

    """
    Induction part
    """
    if if_induction:
        prompt_message = d['messages'][1]['content']
        if not if_transduction_and_induction:
            prompt_message = prompt_message.replace('\n\nThe generated python code is:\n', '')
        response = llm.generate(prompt=d['messages'][1]['content'], num_samples=50, model=VLLMModels.LLAMA31_8B_ins)
        print(response[0])
        if response[0] == "":
            cnt_zero_output += 1
        for j, each_response in enumerate(response):
            try:
                code = each_response.split('```python')[1].split('```')[0].replace('```', '').strip()
            except:
                continue
            
            correct, wrong, re, if_pass  = get_code_answer(test_pur_dataset[cnt]['data'], code, None)
            if if_pass:
                print('PASS in induction ', j)
                pass_task_name.append({'task': test_pur_dataset[cnt]['name'], 'induction iter': j})
                print(pass_task_name)
                break
    if if_pass:
        continue
    """
    Transduction part
    """
    if if_transduction:
        if if_transduction_and_induction:
            transduction_data_system = transduction_data[cnt]['messages'][0]['content']
        else:
            transduction_data_system = transduction_data[cnt]['messages'][0]['content'].replace('[Do transduction directly and generate output]\n', '')
        llm_transduction = LLMClient(provider=Provider.VLLM, system_content=transduction_data_system, cache_dir=args.cache_dir, base_url=args.base_url)

        transduction_data_user = transduction_data[cnt]['messages'][1]['content']
        if not if_transduction_and_induction:
            transduction_data_user = transduction_data_user.replace('\nThe direct output is:\n', '')
        response = llm_transduction.generate(prompt=transduction_data_user, num_samples=50, model=VLLMModels.LLAMA31_8B_ins)
        print(response[0])
        for j, each_response in enumerate(response):
            if each_response == transduction_data[cnt]['messages'][2]['content']:
                print('PASS in transduction ', j)
                pass_task_name.append({'task': test_pur_dataset[cnt]['name'], 'transduction iter': j})
                print(pass_task_name)
                break
        response = llm_transduction.generate(prompt=transduction_data_user, num_samples=0, model=VLLMModels.LLAMA31_8B_ins, temperature=0, cnt=1)
        if response[0] == transduction_data[cnt]['messages'][2]['content']:
            print('PASS in transduction ', j)
            pass_task_name.append({'task': test_pur_dataset[cnt]['name'], 'transduction iter': -1})
            print(pass_task_name)

for item in pass_task_name:
    print(item)

print('cnt_zero_output:', cnt_zero_output)