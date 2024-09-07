import numpy as np

def get_token_prob(logprobs):
    log_prob_list = []
    for j, token_logprob in enumerate(logprobs.content):
      log_prob_list.append(np.exp(token_logprob.logprob)*100)
    return log_prob_list, np.average(np.array(log_prob_list))

def get_all_prob(response):
    average_prob_list = []
    for i, item in enumerate(response):
      logprobs = item.logprobs
      log_prob_list, average_prob = get_token_prob(logprobs)
      average_prob_list.append(average_prob)
    average_prob_list = np.array(average_prob_list)
    sorted_index = np.argsort(average_prob_list)[::-1]
    return average_prob_list, sorted_index