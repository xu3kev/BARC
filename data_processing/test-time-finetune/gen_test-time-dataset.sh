python get_pseudo_eval_task.py
python data_augmentation.py
# change output_huggingface_dataset to the name of the dataset you want to save on hugingface [UserName]/[dataset_name]
python gen_transduction_only_formatted.py --load_file dataset/augmented_test_time_arc_all_evaluation_new_seperate.jsonl --output_huggingface_dataset barc0/test-ttft