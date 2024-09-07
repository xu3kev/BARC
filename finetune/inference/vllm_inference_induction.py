from utils.llm import LLMClient, Provider
import json
from utils.run_code import get_code_answer
import argparse
from utils.vllm_setup import start_model_server
from utils.logger import get_logger
import os

parser = argparse.ArgumentParser()
parser.add_argument('--train_or_evaluate', type=str, default='evaluate', help='train or evaluate')
parser.add_argument('--evaluation_test_all', type=bool, default=True)
parser.add_argument('--cache_dir', type=str, default='cache/llama31_8B_transduction/')
parser.add_argument('--model_name', type=str, default='llama31_8B_transduction')
args = parser.parse_args()

logger = get_logger(f'vllm_inference_{args.model_name}', args)

for arg in vars(args):
    print(arg, getattr(args, arg))

if args.train_or_evaluate == 'evaluate' and args.evaluation_test_all:
    format_testdir = 'data/arc_all_evaluation_string.json'
    original_testdir = 'data/arc_all_evaluation.json'
elif args.train_or_evaluate == 'train':
    format_testdir = 'data/arc_train_wo_seed_string.json'
    original_testdir = 'data/arc_train_wo_seed.json'

process, available_port, base_url = start_model_server(args.model_name)

logger.info(f"Model server started at {base_url}")

with open(format_testdir , 'r') as f:
    data = json.load(f)
system_content = data[0]['messages'][0]['content']


llm = LLMClient(provider=Provider.VLLM, system_content=data[0]['messages'][0]['content'], cache_dir=args.cache_dir, base_url=base_url)

with open(original_testdir, 'r') as f:
    test_pur_dataset = json.load(f)
    
pass_task_name = []
cnt_zero_output = 0
for cnt, d in enumerate(data):
    if_pass = False
    logger.info(f"Current task: {cnt}")
    print(cnt)
    print('pass', len(pass_task_name))

    """
    Induction part
    """
    prompt_message = d['messages'][1]['content']
    for i in range(20, 101, 20):
        response = llm.generate(prompt=d['messages'][1]['content'], num_samples=i, model=f'models/{args.model_name}', logger=logger)
    try:
        response = response.message.content
    except:
        pass
    logger.info(f"Induction response")
    logger.info(response[0].message.content)
    if response[0].message.content == "":
        cnt_zero_output += 1
    for j, each_response in enumerate(response):
        each_response = each_response.message.content
        try:
            code = each_response.split('```python')[1].split('```')[0].replace('```', '').strip()
        except:
            continue
        
        correct, wrong, re, if_pass  = get_code_answer(test_pur_dataset[cnt]['data'], code, None)
        if if_pass:
            logger.info(f"PASS in induction {j}")
            logger.info(pass_task_name)
            logger.info(code)
            logger.info(f"Correct: {correct}")
            print('PASS in induction ', j)
            pass_task_name.append({'task': test_pur_dataset[cnt]['name'], 'induction iter': j})
            if args.train_or_evaluate == 'train':
                os.makedirs(f'new_seeds', exist_ok=True)
                with open(f'new_seeds/{test_pur_dataset[cnt]["name"].split(".")[0]}.py', 'w') as f:
                    f.write(code)
            print(pass_task_name)
            break

for item in pass_task_name:
    print(item)
    logger.info(item)

print('cnt_zero_output:', cnt_zero_output)