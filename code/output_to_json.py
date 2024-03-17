from pathlib import Path
import tempfile

from IPython.display import Image
import requests

from science_parse_api.api import parse_pdf

host = 'http://127.0.0.1'
port = '8080'

import os

folder_path ="D:\eco2"
files_in_folder = os.listdir(folder_path)
pdf_files = [file for file in files_in_folder if file.lower().endswith(".pdf")]

import json
output_folder = "eco2json"
for pdf_file in pdf_files:
    test_pdf_paper = Path(folder_path,f'{pdf_file}').resolve()
    output_dict = parse_pdf(host, test_pdf_paper, port=port)
    output_file_path = "output.json"
    # Convert dictionary to JSON
    json_data = json.dumps(output_dict, indent=4)  # indent is optional for pretty formatting
    file_name = f"output_{pdf_file}.json"
    file_path = os.path.join(output_folder, file_name)
    with open(file_path, "w") as json_file:
        json_file.write(json_data)

# pp = pprint.PrettyPrinter(indent=4)

# pp.pprint(output_dict)