from utils.llm import LLMClient, Provider,VLLMModels
import json
from utils.run_code import get_code_answer
import argparse
from utils.vllm_setup import start_model_server
from utils.logger import get_logger
from openai import OpenAI
from utils.log_probs import get_all_prob

parser = argparse.ArgumentParser()
parser.add_argument('--train_or_evaluate', type=str, default='evaluate', help='train or evaluate')
parser.add_argument('--evaluation_test_all', type=bool, default=True)
parser.add_argument('--cache_dir', type=str, default='cache/llama31_8B_transduction/')
parser.add_argument('--model_name', type=str, default='llama31_8B_transduction')
args = parser.parse_args()

logger = get_logger(f'vllm_inference_{args.model_name}_beamsearch', args)

for arg in vars(args):
    print(arg, getattr(args, arg))

if args.train_or_evaluate == 'evaluate' and args.evaluation_test_all:
    original_testdir = 'data/arc_all_evaluation.json'
    transduction_dir = 'data/arc_all_evaluation_direct_string.json'
# elif args.train_or_evaluate == 'train':
#     original_testdir = '../test_dataset/original_dataset/arc_train_wo_seed.json'
#     transduction_dir = '../test_dataset/train_direct_old.json'

process, available_port, base_url = start_model_server(args.model_name)

logger.info(f"Model server started at {base_url}")

with open(transduction_dir, 'r') as f:
    transduction_data = json.load(f)

with open(original_testdir, 'r') as f:
    test_pur_dataset = json.load(f)
    
pass_task_name = []
cnt_zero_output = 0
for cnt, d in enumerate(transduction_data):
    if_pass = False
    logger.info(f"Current task: {cnt}")
    """
    Transduction part
    """
    logger.info(f"Transduction task")
    transduction_data_system = transduction_data[cnt]['messages'][0]['content']
    llm_transduction = LLMClient(provider=Provider.VLLM, system_content=transduction_data_system, cache_dir=args.cache_dir, base_url=base_url)

    transduction_data_user = transduction_data[cnt]['messages'][1]['content']
    response = llm_transduction.generate(prompt=transduction_data_user, num_samples=1, model=f"models/{args.model_name}", logger=logger, beam_search=True, best_of=3)

    logger.info(len(response))
    logger.info(response[0].message.content)
    for each_response in response:
        if each_response.message.content.replace('```', '') == transduction_data[cnt]['messages'][2]['content'].replace('```', ''):
            logger.info(f"PASS in transduction")
            pass_task_name.append({'task': test_pur_dataset[cnt]['name']})
            break

for item in pass_task_name:
    print(item)
    logger.info(item)

print('cnt_zero_output:', cnt_zero_output)