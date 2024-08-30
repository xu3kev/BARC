## Llamafactory Setup
#### Llamafactory installation:

```
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

#### Finetune Steps

##### Single GPU
- Step 1: Add dataset into file `LLamaFactory/data/`

  - In Open-AI format

    ```
    [
      {
        "messages": [
          {
            "role": "system",
            "content": "system prompt (optional)"
          },
          {
            "role": "user",
            "content": "human instruction"
          },
          {
            "role": "assistant",
            "content": "model response"
          }
        ]
      }
    ]
    ```

  - Edit `dataset_info.json` file

    ```
      "your_dataset_name": {
      "file_name": "your_dataset_name.json",
      "formatting": "sharegpt",
      "columns": {
        "messages": "messages"
      },
      "tags": {
        "role_tag": "role",
        "content_tag": "content",
        "user_tag": "user",
        "assistant_tag": "assistant",
        "system_tag": "system"
      }
    },
    ```

- Step 2: Edit `Llama31_8B_lora_sft.yaml`

  - dataset:  `dataset=your_dataset_name`
  - Template: refer to https://github.com/hiyouga/LLaMA-Factory/blob/main/README.md "Supported Models"
  - finetuning_type: `lora, qlora, full`
  - output_dir: `saves/Llama31_8B_lora_sft` or whatever model you like
  - save_steps: save checkpoint per `save_steps`
  - logging_steps: logging per `logging_steps`
  - eval_steps: evaluate on validation set per `eval_steps`

```
llamafactory-cli train your_path/Llama31_8B_lora_sft.yaml
```

The example of  `Llama31_8B_lora_sft.yaml` is in `sft/`

After finetuning, the model will be in your output directory.

##### Multiple GPUs

Run the sub script in `sub/train_llama31_distribution.sub`

#### Inference Steps

- **Step 1: Merge lora results**

  Edit `llama31_lora_sft.yaml`, change `adapter_name_or_path` into `output_dir`, change `export_dir` to wherever you want to store it.

  The example of  `llama31_lora_sft.yaml` is in file `merge/`

  ```
  llamafactory-cli export examples/merge_lora/llama31_lora_sft.yaml
  ```

- **Step 2: run vllm**

  Edit `llama31_vllm.yaml`, change `model_name_or_path` into output_dir in `examples/merge_lora/llama31_lora_sft.yaml`

  The example of  `llama31_vllm.yaml` is in `inference/`

  ```
  python vllm_inference.py
  ```