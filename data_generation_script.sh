# This resets the problem generation state by deleting everything---helpful if you want to start from scratch but be careful!
# rm -rf generated_descriptions generated_code generated_problems

# First we generate natural language descriptions of problems
# We do this in batches of 1000, producing 10 new descriptions with each batch, iterating through 10 different seeds
# The final output we're after is 100k descriptions
# Executing this script will produce files in generated_descriptions of the form:
#           generated_descriptions/self_instruct_descriptions_fewshot_75_gpt-4_temp0.70_maxtokens1024_rng[0-9]*_used_concepts.jsonl
mkdir -p generated_descriptions
for rng_offset in {0..10}; do python generate_descriptions.py --outdir generated_descriptions --batch_request --model gpt-4 --num_generations 10 --max_tokens 1024 --batch_size 1000 --num_descriptions 75 --rng_offset $rng_offset; done

# Next we use the RAG model, using batching. 
# You don't have to keep tack of the intermediate files because it's smart about handling the batching for you
# We do this both with suggesting functions, and without, to get diversity
mkdir -p generated_code
for filename in `ls generated_descriptions/*jsonl`; do python generate_code.py                    --outdir generated_code --batch_request --ignore_cache_samples --prompt_model gpt-4o-mini -n 16 -s 4 --nohtml --jsonl $filename; done
for filename in `ls generated_descriptions/*jsonl`; do python generate_code.py --suggest_function --outdir generated_code --batch_request --ignore_cache_samples --prompt_model gpt-4o-mini -n 16 -s 4 --nohtml --jsonl $filename; done

# This will generate files of the form generated_code/self_instruct_code_fewshot_4_gpt-4o-mini_temp0.70_maxtokens2048_briefcommon_description_file_generated_descriptions_self_instruct_descriptions_fewshot_75_gpt-4_temp0.70_maxtokens1024_rng*.jsonl

# run problem generation script on everything in the directory, producing output in generated_problems
mkdir -p generated_problems
for filename in `ls generated_code/*jsonl`; do python generate_problems.py --jsonl $filename --outdir generated_problems; done

# if you want to you can visualize them like this, but this step is totally optional
mkdir -p generated_problems/visualized
for filename in `ls generated_problems/*jsonl`; do python visualize.py --jsonl $filename --outdir generated_problems/visualized; done