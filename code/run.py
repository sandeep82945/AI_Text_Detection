import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')
import yaml
tokenizer = PunktSentenceTokenizer()
from test_preprocessing import preprocess
from anthropic_bedrock import AnthropicBedrock, HUMAN_PROMPT, AI_PROMPT

from tqdm import tqdm
from gemini import inference as gemini_inference  #keep changing
#from claude import inference as claude_inference
#from galactica import inference as galactica_inference

with open('code/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

paper_dump_path = config["paper_dump_path"]
input_folder = config["input_folder"]
model_name = config["model_name"]
domain = input_folder.split('/')[-1]


dump_folder = os.path.join(paper_dump_path,model_name, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

#Change this for each models
def generate_gemini(paper_text):
    prompt = f"""Imagine you are a research scientist, read the following paper and generate top 5 possible future research ideas after brainstroming:  
        ``` {paper_text}```
        5 possible future research ideas from the paper are: """

    response = gemini_inference(prompt)
    return response

def generate_claude2(paper_text):
    prompt = f"""{HUMAN_PROMPT} Imagine you are a research scientist, read the following paper and generate top 5 possible future research ideas after brainstorming:  
        {paper_text}
        5 possible future research ideas from the paper are: {AI_PROMPT}"""
    response = claude_inference(prompt)
    return response

def generate_galactica(paper_text):
    prompt = f""" Imagine you are a research scientist, read the following paper and generate 5 possible future research ideas after brainstorming:  
        {paper_text[0:1000]+paper_text[-1000:]}
        5 possible future research ideas from the paper are: <work>:"""
    response = galactica_inference(prompt)
    return response

def choose_model(text):
    if model_name == 'gemini':
        return generate_gemini(text)
    elif model_name == 'claude':
        return generate_claude2(text)

for filename in tqdm(os.listdir(input_folder)):
    if not filename.endswith('.txt'):
        continue
    dump_filename = os.path.join(dump_folder, filename)

    if os.path.exists(dump_filename):
            continue
    
    reponse = ''
    filepath = os.path.join(input_folder,filename)
    with open(filepath, 'r') as f:
         text = f.read()
         text = text.replace('\n', ' ')
         response = preprocess(text)
         response = choose_model(response)
         if response is None:
             continue

    with open(dump_filename, 'w') as f:
        f.write(response)