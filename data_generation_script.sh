# First we generate natural language descriptions of problems
# We do this in batches of 1000, producing 10 new descriptions with each batch, iterating through 10 different seeds
# The final output we're after is 100k descriptions
# Executing this script will produce files of the form:
#           batch_requests_self_instruct_descriptions_fewshot_75_gpt-4_temp0.70_maxtokens1024_rng[0-9]_used_concepts.jsonl
# Upload those to OpenAI
for rng_offset in {0..9}; do python description_prompt.py --model gpt-4 --num_generations 10 --max_tokens 1024 --batch_size 1000 --num_descriptions 75 --rng_offset $rng_offset; done

# Wait until it's done...
# ...download everything into the generated_descriptions directory

# Next we use the RAG model, using batching. 
# You don't have to keep tack of the intermediate files because it's smart about handling the batching for you
for filename in `ls generated_descriptions`; do python problem_from_description_prompt.py --batch_request --ignore_cache_samples --prompt_model gpt-4o-mini -n 16 -s 4 --nohtml --jsonl generated_descriptions/"$filename"; done