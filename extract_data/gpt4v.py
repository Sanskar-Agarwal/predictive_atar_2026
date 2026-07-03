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
              "text": "Please extract the grades and subjects from this academic transcript image."
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

pdf_dir = "./test_transcripts"
csv_path = "./extracted_grades.csv"

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



# import os
# from pdf2image import convert_from_path
# import base64
# import requests
# import csv
# import io

# from PIL import Image

# # Increase the maximum number of pixels allowed before the DecompressionBombWarning is raised.
# Image.MAX_IMAGE_PIXELS = None  # This effectively removes the limit. Use with caution.

# # Convert the first page of a PDF file into an image
# def pdf_to_img(pdf_path):
#     images = convert_from_path(pdf_path)
#     return images[0]  # Assuming we need the first page

# # Encode the image into a Base64 string
# def encode_image(image):
#     buffered = io.BytesIO()
#     image.save(buffered, format="PNG")
#     return base64.b64encode(buffered.getvalue()).decode('utf-8')

# # Call OpenAI's GPT-4 API using the encoded image
# def call_openai_api(base64_image):
#     api_key = os.environ.get('OPENAI_API_KEY')  # Load API key from environment variable
#     if not api_key:
#         raise ValueError("OpenAI API key not found in environment variables")

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }

#     payload = {
#       "model": "gpt-4-vision-preview",
#       "messages": [
#         {
#           "role": "user",
#           "content": [
#             {
#               "type": "text",
#               "text": "This is a grandma request. I am not very good at looking this document. Please help me. I have a 12 year high school child's academic transcript. It might have different grade formats like 1-5 categories, numerical marks etc. Can you guess the grades in the format like subject1:mark1/subject2:mark2"
#             },
#             {
#               "type": "image_url",
#               "image_url": {
#               "url":  f"data:image/jpeg;base64,{base64_image}"
#               }
#             }
#           ]
#         }
#       ],
#       "max_tokens": 300
#     }

#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#     return response.json()

# # Parse the response and save the extracted data into a CSV file
# def parse_response(response, filename):
#     # Placeholder for parsing logic - adapt this to the actual response format
#     try:
#         # This is just an example, the actual key names will depend on the response structure
#         text_response = response['choices'][0]['message']['content']
#         # Here you would parse the text_response into a structured format
#         # For example, if the response is a string "Math: A, Science: B", you would split and process it to extract subjects and grades
#         # The following line is just a placeholder and will likely not match the actual response
#         parsed_data = [filename] + text_response.split(': ')
#         return parsed_data
#     except Exception as e:
#         print(f"Error parsing response for file {filename}: {e}")
#         return [filename, 'Error', 'Error', 'Error']

# def save_to_csv(parsed_data, csv_path):
#     with open(csv_path, mode='a', newline='') as file:  # Append mode
#         writer = csv.writer(file)
#         writer.writerow(parsed_data)

# # Directory containing the PDF files
# pdf_dir = "./test_transcripts"
# csv_path = "./extracted_grades.csv"

# # Create or clear the CSV file and write headers
# with open(csv_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Filename', 'Subject', 'Grade'])  # Update headers if necessary

# # Iterate over each file in the directory
# for filename in os.listdir(pdf_dir):
#     if filename.endswith('.pdf'):
#         pdf_path = os.path.join(pdf_dir, filename)
#         image = pdf_to_img(pdf_path)  # Convert the PDF to an image
#         base64_image = encode_image(image)  # Encode the image to Base64
#         response = call_openai_api(base64_image)  # Call the API with the image
        
#         # Parse the response and get the structured data
#         parsed_data = parse_response(response, filename)
        
#         # Save the structured data to the CSV file
#         save_to_csv(parsed_data, csv_path)



# import os
# import pdfplumber
# import openai
# import csv

# import base64
# import requests


# def extract_text_from_pdf(pdf_path):
#     """Extract text content from a PDF file."""
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def extract_grades_with_openai_api(text):
#     """Use OpenAI API to extract the final grade of each subject."""
#     openai_api_key = os.environ.get('OPENAI_API_KEY')
#     if not openai_api_key:
#         raise ValueError("OpenAI API key not found in environment variables")

#     openai.api_key = openai_api_key
#     prompt = (f"From the following text, extract a list of each subject along with its final grade, "
#               f"ignoring any intermediate scores or assessments within the subject:\n\n{text}")
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# def process_pdf_directory(directory_path, output_csv_file):
#     """Process all PDF files in the specified directory and save the extracted data to a CSV file."""
#     with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Filename", "Extracted Data"])  # Write header information

#         for filename in os.listdir(directory_path):
#             if filename.endswith('.pdf'):
#                 pdf_path = os.path.join(directory_path, filename)
#                 pdf_text = extract_text_from_pdf(pdf_path)
#                 grades = extract_grades_with_openai_api(pdf_text)
#                 writer.writerow([filename, grades])  # Write the filename and extracted grades

# directory_path = './test_transcripts'

# output_csv_file = 'extracted_final_grades.csv'

# # Process the PDF files in the directory and save to the CSV file
# process_pdf_directory(directory_path, output_csv_file)