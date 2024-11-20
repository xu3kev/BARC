This framework adopted from [The Alignment Handbook](https://github.com/huggingface/alignment-handbook)

## Installation instructions

To run the code in this project, first, create a Python virtual environment using e.g. Conda:

```shell
conda create -n handbook python=3.10 && conda activate handbook
```

Next, install PyTorch `v2.4`

You will also need Flash Attention 2 installed, which can be done by running:

```shell
python -m pip install flash-attn --no-build-isolation
```

You can then install the remaining package dependencies as follows:

```shell
git clone https://github.com/huggingface/alignment-handbook.git
cd ./alignment-handbook/
python -m pip install .
```

Next, log into your Hugging Face account as follows:

```shell
huggingface-cli login
```

You'll also need to log in with wandb:

```shell
wandb login
```

## Recipe

Please see the yaml files under `recipes` for example of training induction and transduction models.

```bash
ACCCELERATE_LOG_LEVEL=info accelerate launch --config_file recipes/accelerate_configs/deepspeed_zero3.yaml --num_processes=8 scripts/run_sft.py recipes/$RECEIPE.yaml --load_in_4bit=false
```
