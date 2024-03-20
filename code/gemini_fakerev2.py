import os
import yaml
import json
from tqdm import tqdm
from gemini import inference as gemini_inference

with open('/content/AI_Text_Detection/code/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

paper_dump_path = config["paper_dump_path"]
input_folder = config["input_folder"]
model_name = config["model_name"]
domain = input_folder.split('/')[-1]
dump_folder = os.path.join(paper_dump_path, model_name, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

def generate_gemini(paper_text, paper_title):
    prompt = f"""Imagine you are a research scientist, read the following paper and write a peer review in the following format:  
        1) Summary (Write a concise summary outlining the paper's topic and main contributions. Highlight the significance of the research problem addressed, any novel methods or techniques introduced, and the key findings or results obtained. Provide enough detail to give readers a clear understanding of the paper's contribution to its field.)
        2) Soundness
        3) Presentation
        4) Contribution
        5) Strengths
        6) Weaknesses
        7) Questions
        8) Flag for Ethics Review
        9) Rating
        10) Confidence
        11) Code of Conduct 
        ``` {paper_text}```
        """
    response = gemini_inference(prompt)
    return response

def choose_model(text, paper_title):
    if model_name == 'gemini':
        return generate_gemini(text, paper_title)
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
    
    paper_title = data.get('title', 'Untitled')

    response = choose_model(full_text, paper_title)
    if response is None:
        continue

    with open(dump_filename, 'w') as f:
        f.write(response)
