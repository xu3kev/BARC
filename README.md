# Bootstrapping ARC: Synthetic Problem Generation for ARC Visual Reasoning Tasks

This repository provides tools for generating synthetic [ARC](https://arcprize.org/) problems, which consist of input/output grid pairs corresponding to transformation rules defined by Python code.

🤗[[Synthetic Dataset]](https://huggingface.co/collections/barc0/synthetic-arc-dataset-6725aa6031376d3bacc34f76)
🤗[[Synthetic Dataset in Instruction Format]](https://huggingface.co/collections/barc0/synthetic-arc-dataset-prompt-formatted-67223d0e7c232af8ed782b37)

## Seed Problems
The repository contains 162 manually written solutions corresponding to problems from the [ARC training set](https://github.com/fchollet/ARC/tree/master/data/training). These manually written seeds are under the `seeds/` folder and utilize shared utility functions from `seeds/common.py`, which provides common routines important to multiple ARC problems like grid or objects manipulation operations.

Each seed problem is a Python file with the following structure:

```python
from common import *  # Shared utilities for grid manipulation
import numpy as np

# Concept Labels:
# <List of core concepts used in this problem, e.g., pattern repetition, scaling, color mapping>

# Description:
# <Natural language description of the transformation rule from input grid to output grid>

def main(input_grid):
   # Solution: transformation function that solves the problem
   # Takes a 2D numpy array as input and returns a 2D numpy array as output
   ...
   return output_grid

def generate_input():
   # Input generator: randomly generates valid input grids for this problem
   # Returns a 2D numpy array representing a valid input grid
   ...
   return input_grid
```

## Synthetic Data Generation
🤗[[Synthetic Dataset]](https://huggingface.co/collections/barc0/synthetic-arc-dataset-6725aa6031376d3bacc34f76)
🤗[[Synthetic Dataset in Instruction Format]](https://huggingface.co/collections/barc0/synthetic-arc-dataset-prompt-formatted-67223d0e7c232af8ed782b37)

Visualization examples of our synthetic dataset: 🎊[[BARC Dataset Examples]](https://www.basis.ai/arc_interface/examples) visualized by [Michi](https://naiimic.github.io/) from [Basis](https://www.basis.ai/our-work/) 



The synthetic data generation pipeline takes the seed problems and remixes them using LLM to generate new problems. Each generated problem includes both a solution (transformation function) and input generator, which are executed to create input/output grid pairs forming an ARC problem.

The pipeline consists of three stages:

- `generate_descriptions.py`: Generate natural language descriptions of synthetic problems from seed descriptions
- `generate_code.py`: Generate solution and input generator code using the descriptions and similar seed examples (via RAG)
- `generate_problems.py`: Execute the generated code to create concrete ARC problems

See `data_generation_script.sh` for an example of complete pipeline execution using GPT-4 for description generation and GPT4o-mini for code generation.


## Finetuning
🤗[[Models]](https://huggingface.co/collections/barc0/llm-for-arc-672247e813fd817f56c35eee)
🤗[[Test-Time-Finetune Adapters]](https://huggingface.co/collections/barc0/lora-file-for-transduction-test-time-finetune-6725a8558baabd079b889596)


We adopted https://github.com/huggingface/alignment-handbook.git framework to finetune Llama models. See `finetune/alignment-handbook/README.md` for more details, and `finetune/alignment-handbook/recipes/barc` for example recipes. We provide finetune script and models for both "transduction" and "induction" methods:

* Induction: induction models is finetuned to output the solution code given the ARC problems.
* Transduction: transduction models is finetuned to directly output the test output grids given the problem.

We finetune with pure text models, and convert the input grids into string format like
```
Gray Black Black Gray Black
Gray Black Black Gray Black
Gray Black Gray Gray Gray
Gray Gray Gray Black Black
Black Black Gray Black Black
```
Numbers 0-9 are maps are converted to "Black", "Blue", "Red", "Green", "Yellow", "Gray", "Pink", "Orange", "Purple", and "Brown" respectively.
For the detail prompt template please see the script which converts the problems to their corresponding prompt format, e.g. `finetune/alignment-handbook/gen_test_prompt.py` and `finetune/alignment-handbook/gen_dataset_both.py`.

For transduction test-time finetuning and Potpourri version, we include a pseudo evaluation dataset and formatted [RE-ARC](https://github.com/michaelhodel/re-arc)  dataset here: 

The script for generating test-time finetuning can be found here: https://github.com/xu3kev/BARC/blob/master/data_processing/test-time-finetune/gen_test-time-dataset.sh

🤗[[Supplementary Dataset]](https://huggingface.co/collections/barc0/supplementary-dataset-prompt-formatted-67265caca53d5d0e84330c0e)

## Inference

We provide an example script using vllm for inference of the model, please edit the script accordingly.
* Induction: See `finetune/inference/vllm_inference.py`

* Transduction for evaluation dataset: See `finetune/inference/vllm_inference_transduction_evaluation.py`

* Transduction for conceptARC dataset:

  ``finetune/inference/vllm_inference_transduction_concept_arc.py``

## Evaluation

For transduction, evaluation can be done by directly compare the input grid and output grid.
For induction, the samples code needed to be executed and get the results. We provide the execution code at `eval_code_samples.py`

## Environment Setup

#### Finetune model setup

```
# Set up a new conda environment
git clone https://github.com/xu3kev/BARC.git
conda create -n handbook python=3.10
conda activate handbook

pip install torch==2.4
pip install flash-attn --no-build-isolation

# download corresponding package
cd BARC/finetune/alignment-handbook/
python -m pip install .
```

If there is an error when build flash-attn, try this instead, you may need to modify the package pytorch/python/cuda version
```
wget https://github.com/Dao-AILab/flash-attention/releases/download/v2.5.8/flash_attn-2.5.8+cu118torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
pip install flash_attn-2.5.8+cu118torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl --no-build-isolation
```

Login to wandb and huggingface

```
huggingface-cli login
wandb login
```

Run finetune command, you can change `num_processes` to the gpus you have.

```
cd BARC/finetune/alignment-handbook/
ACCELERATE_LOG_LEVEL=info accelerate launch --config_file recipes/accelerate_configs/deepspeed_zero3.yaml --num_processes=8 scripts/run_sft.py recipes/barc/transduction_config_fft_engineer_heavy_model.yaml --load_in_4bit=false
```

#### Inference setup

* Induction: `vllm==0.6.0`
* Transduction: `vllm==0.5.4`

### Inference Samples
We provide inference samples
* Induction (ARC-Potpourri 20k samples) 🤗[[Samples]](https://huggingface.co/barc0/induction_samples_with_execution_results/tree/main)

- Transduction output original results for evaluation dataset and ConceptARC dataset 🤗[[Samples]](https://huggingface.co/datasets/barc0/transduction_experimental_results)

- Transduction and induction output examples visualization: 🎊 [[Visualization]](https://www.basis.ai/arc_interface/arc) visualized by [Michi](https://naiimic.github.io/) from [Basis](https://www.basis.ai/our-work/)

### Evaluation
We provide an example script (`evaluation.py`) that scores inference samples and execution results. The script also demonstrates how we ensemble two models and calculate the scores.
(requires `pip install -r requirements.txt`)

### Citation

If you find our method, models, and dataset helpful, please kindly cite our paper :)

```
@misc{li2024combininginductiontransductionabstract,
      title={Combining Induction and Transduction for Abstract Reasoning}, 
      author={Wen-Ding Li and Keya Hu and Carter Larsen and Yuqing Wu and Simon Alford and Caleb Woo and Spencer M. Dunn and Hao Tang and Michelangelo Naim and Dat Nguyen and Wei-Long Zheng and Zenna Tavares and Yewen Pu and Kevin Ellis},
      year={2024},
      eprint={2411.02272},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2411.02272}, 
}
```
