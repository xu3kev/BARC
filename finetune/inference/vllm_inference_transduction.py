# from inference.utils.llm_wd import LLMClient, Provider,VLLMModels
import json
from utils.run_code import get_code_answer
import argparse
from utils.vllm_setup import start_model_server
from utils.logger import get_logger
from openai import OpenAI
from utils.log_probs import get_all_prob
from utils.llm.main import get_llm
from utils.transform_str_into_list import transform_str_into_list, count_differences

parser = argparse.ArgumentParser()
parser.add_argument('--train_or_evaluate', type=str, default='evaluate', help='train or evaluate')
parser.add_argument('--evaluation_test_all', type=bool, default=True)
parser.add_argument('--cache_dir', type=str, default='cache/llama31_8B_transduction/')
parser.add_argument('--model_name', type=str, default='llama31_8B_transduction')
parser.add_argument('--llm-temperature', type=float, default=0.0, help="The temperature to use for LLM")
parser.add_argument('--llm-seed', type=int, default=None, help="The seed to use for LLM")

args = parser.parse_args()

logger = get_logger(f'vllm_inference_{args.model_name}_beamsearch', args)

for arg in vars(args):
    print(arg, getattr(args, arg))

if args.train_or_evaluate == 'evaluate' and args.evaluation_test_all:
    original_testdir = 'data/arc_all_evaluation.json'
    transduction_dir = 'data/arc_all_evaluation_direct_string.json'
elif args.train_or_evaluate == 'train':
    original_testdir = 'data/arc_train_wo_seed.json'
    transduction_dir = 'data/train_direct_wo_seed.json'

process, available_port, base_url = start_model_server(args.model_name)

logger.info(f"Model server started at {base_url}")

with open(transduction_dir, 'r') as f:
    transduction_data = json.load(f)

with open(original_testdir, 'r') as f:
    test_pur_dataset = json.load(f)
    
pass_task_name = []
cnt_zero_output = 0
llm_transduction  = get_llm(args, base_url)

less_than_than_3 = 0
for cnt, d in enumerate(transduction_data):
    if_pass = False
    logger.info(f"Current task: {cnt}")
    """
    Transduction part
    """
    logger.info(f"Transduction task")

    if "[Do transduction directly and generate output]\n" not in transduction_data[cnt]['messages'][0]['content']:
        transduction_data_system = "[Do transduction directly and generate output]\n" + transduction_data[cnt]['messages'][0]['content']
    else:
        transduction_data_system = transduction_data[cnt]['messages'][0]['content']
    

    # llm_transduction = LLMClient(provider=Provider.VLLM, system_content=transduction_data_system, cache_dir=args.cache_dir, base_url=base_url)
    
    transduction_data_user = transduction_data[cnt]['messages'][1]['content']
    prompt = [
        {'role': 'system', 'content': transduction_data_system},
        {'role': 'user', 'content': transduction_data_user},
    ]
    try:
        response = llm_transduction(prompt=prompt, model_args={'n': 100, 'max_tokens': 800, 'extra_body':{'use_beam_search': True, "best_of": 1000, 'top_p': 1.0}}).choices
    except Exception as e:
        print(e)
        continue
    # response = llm_transduction.generate(prompt=transduction_data_user, num_samples=3, model=f"models/{args.model_name}", logger=logger, beam_search=True, best_of=100)

    # logger.info(len(response))
    # logger.info(response[0].message.content.replace('```', ''))
    # logger.info(transduction_data[cnt]['messages'][2]['content'])
    min_response = 10000000000
    for i in range(100):
        each_response = response[i].message.content
        logger.info(each_response)
        if each_response.replace('```', '').strip() == transduction_data[cnt]['messages'][2]['content'].replace('```', '').strip():
            logger.info(f"PASS in transduction {i}")
            pass_task_name.append({'task': test_pur_dataset[cnt]['name']})
            break
        each_response = each_response.replace('```', '').replace('Output:', '').strip()
        diff = count_differences(transform_str_into_list(each_response), transform_str_into_list(transduction_data[cnt]['messages'][2]['content'].replace('```', '').strip()))
        if diff < min_response and diff != -1:
            min_response = diff
        logger.info(f"diff: {diff}")
        
    if min_response <= 3:
        less_than_than_3 += 1
    # for each_response in response:
    # if each_response.message.content.replace('```', '').strip() == transduction_data[cnt]['messages'][2]['content'].replace('```', ''):

    #     logger.info(f"PASS in transduction")
    #     pass_task_name.append({'task': test_pur_dataset[cnt]['name']})

print('less_than_than_3:', less_than_than_3)
for item in pass_task_name:
    print(item)
    logger.info(item)

print('cnt_zero_output:', cnt_zero_output)