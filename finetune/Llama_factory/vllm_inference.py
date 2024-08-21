from utils.llm import LLMClient, Provider,VLLMModels
import json
from utils.run_code import get_code_answer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='llama31_both-checkpoint-1300')
parser.add_argument('--format_testdir', type=str, default='test_dataset/arc_test_50_wending_string.json')
parser.add_argument('--original_testdir', type=str, default='test_dataset/arc_test_50.json')
parser.add_argument('--cache_dir', type=str, default='cache/llama31/')
parser.add_argument('--base_url', type=str, default="http://localhost:8000/v1")

args = parser.parse_args()
with open(args.format_testdir , 'r') as f:
    data = json.load(f)

llm = LLMClient(provider=Provider.VLLM, system_content=data[0]['messages'][0]['content'], cache_dir=args.cache_dir, base_url=args.base_url)

with open(args.original_testdir, 'r') as f:
    test_pur_dataset = json.load(f)

pass_task_name = []

for cnt, d in enumerate(data):
    print(cnt)
    for i in range(200, 1001, 100):
        response = llm.generate(prompt=d['messages'][1]['content'], num_samples=i, model=VLLMModels.LLAMA31_8B_ins)
    print(response[0])
    for j, each_response in enumerate(response):
        try:
            code = each_response.split('```python')[1].split('```')[0].replace('```', '').strip()
        except:
            continue
        
        correct, wrong, re, if_pass  = get_code_answer(test_pur_dataset[cnt]['data'], code, None)
        # print('correct:', len(correct), 'wrong:', len(wrong), 're:', len(re), 'if_pass:', if_pass)
        if if_pass:
            print('PASS in ', j)
            pass_task_name.append({'task': test_pur_dataset[cnt]['name'], 'iter': j})
            break

for item in pass_task_name:
    print(item)


