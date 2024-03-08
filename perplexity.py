from openai import OpenAI


# model = 'openai'

# client = OpenAI(api_key='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')

# openai_model = 'gpt-3.5-turbo'
# import numpy as np
# import torch
import numpy as np
# # assert openai_key is not None, "Must provide OpenAI API key as --openai_key"
client = OpenAI(api_key='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')

def get_ll(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        ,logprobs = True
        )
    result = response.choices[0]
    tokens, logprobs = result.message.content, result.logprobs
    all_log_prob = [item.logprob for item in logprobs.content]
    final_perplexity = np.mean(all_log_prob)

    # print(result.logprobs)
    print(tokens)
    print(final_perplexity)
    
    
    # if model == 'openai':        
    #     #kwargs = { "model": openai_model, "temperature": 0, "max_tokens": 0, "echo": True, "logprobs": 0}
    #     r = client.completions.create(model= openai_model,
    #     messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "Who won the world series in 2020?"},
    #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #     {"role": "user", "content": "Where was it played?"}
    #     ])
        
    #     result = r.choices[0]
    #     tokens, logprobs = result["logprobs"]["tokens"][1:], result["logprobs"]["token_logprobs"][1:]

    #     assert len(tokens) == len(logprobs), f"Expected {len(tokens)} logprobs, got {len(logprobs)}"

    #     return np.mean(logprobs)
    # else:
    #     with torch.no_grad():
    #         tokenized = base_tokenizer(text, return_tensors="pt").to(DEVICE)
    #         labels = tokenized.input_ids
    #         return -base_model(**tokenized, labels=labels).loss.item()

get_ll("hi hello")


from openai import OpenAI
client = OpenAI(api_key='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')

