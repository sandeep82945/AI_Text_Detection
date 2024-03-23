import json
import os
import requests

def download_pdfs_from_json(json_file, output_folder):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    i = 0

    for entry in data:
        paper_link = entry.get('Paper Link')
        if paper_link:
            i += 1
            print("Downloading file:", i)

            # Get response object for the PDF link

            if paper_link.split('=')[-1]+'.pdf' in list(os.listdir(output_folder)):
                continue

            response = requests.get(paper_link)

            # Extract PDF name from the URL and create a local file
            pdf_name = os.path.join(output_folder, f"{paper_link.split('=')[-1]}.pdf")
            with open(pdf_name, 'wb') as pdf_file:
                pdf_file.write(response.content)

            print("File", i, "downloaded")

# Example Usage:
json_file_path = "/Users/sandeepkumar/AI_detection/AI_Text_Detection/data_creation.py/paper_reviews2.json"
output_folder_path = "/Users/sandeepkumar/AI_detection/AI_Text_Detection/data/EMNLP_PDFS"
download_pdfs_from_json(json_file_path, output_folder_path)
