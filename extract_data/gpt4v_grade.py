import os
from pdf2image import convert_from_path
import base64
import requests
import csv
import io
from PIL import Image

# Increase the max image pixels
Image.MAX_IMAGE_PIXELS = None

def pdf_to_imgs(pdf_path):
    return convert_from_path(pdf_path)

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def call_openai_api(base64_image):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Please extract the grades and subjects from this academic transcript image. If one image contain the subject name, it must has a grade"
            },
            {
              "type": "image_url",
              "image_url": {
              "url":  f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def parse_response(response, filename, page_number):
    try:
        text_response = response['choices'][0]['message']['content']
        parsed_data = [filename, page_number] + text_response.split(': ')
        return parsed_data
    except Exception as e:
        print(f"Error parsing response for file {filename}, page {page_number}: {e}")
        return [filename, page_number, 'Error']

def save_to_csv(parsed_data, csv_path):
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(parsed_data)

pdf_dir = "./transcripts_grade"
csv_path = "./transcripts_grade/extracted_grades.csv"

with open(csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Page', 'Subject', 'Grade'])

for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        images = pdf_to_imgs(pdf_path)
        for page_number, image in enumerate(images, start=1):
            base64_image = encode_image(image)
            response = call_openai_api(base64_image)
            parsed_data = parse_response(response, filename, page_number)
            save_to_csv(parsed_data, csv_path)