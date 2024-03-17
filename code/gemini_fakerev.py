import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')
import yaml
from tqdm import tqdm
from gemini import inference as gemini_inference
# from test_preprocessing import preprocess

tokenizer = PunktSentenceTokenizer()

with open('/content/AI_Text_Detection/code/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

paper_dump_path = config["paper_dump_path"]
input_folder = config["input_folder"]
model_name = config["model_name"]
domain = input_folder.split('/')[-1]
dump_folder = os.path.join(paper_dump_path, model_name, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

def generate_gemini(paper_text):
    prompt = f"""Imagine you are a research scientist, read the following paper and write a peer review in the following format:  
        1) Title - 
        2) Main Contributions
        3) Reasons to accept
        4) Reasons to reject
        5) Questions to authors
        6) Soundness - a value between (1 - 5) and write 1-2 lines.
        7) Excitment - a value between (1 - 5) and write 1-2 lines.
        8) Reproducibility - a value between (1 - 5) and write 1-2 lines.
        9) Ethical Concerns 
        10) Reviewer Confidence - a value between (1 - 5) and write 1-2 lines.
        ``` {paper_text}```
        """

    response = gemini_inference(prompt)
    return response

def choose_model(text):
    if model_name == 'gemini':
        return generate_gemini(text)
    elif model_name == 'claude':
        return generate_claude2(text)

for filename in tqdm(os.listdir(input_folder)):
    if not filename.endswith('.pdf.json'):
        continue
    
    dump_filename = os.path.join(dump_folder, os.path.splitext(filename)[0] + '.txt')

    if os.path.exists(dump_filename):
        continue
    
    with open(os.path.join(input_folder, filename), 'r') as json_file:
        data = json.load(json_file)

    full_text = ''
    for section in data.get('sections', []):
        full_text += section.get('text', '') + '\n'

    # response = preprocess(full_text)
    response = choose_model(full_text)
    if response is None:
        continue

    with open(dump_filename, 'w') as f:
        f.write(response)
