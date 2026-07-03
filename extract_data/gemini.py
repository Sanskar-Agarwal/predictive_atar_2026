import pathlib
import textwrap
from pdf2image import convert_from_path
import google.generativeai as genai
import os
import PIL.Image

def pdf_to_imgs(pdf_path):
    return convert_from_path(pdf_path,dpi=25)

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')
# img_url = os.path.join(BASE_DIR, 'extract_data','test_transcripts','transcript.png')
# img = PIL.Image.open(img_url)
# response = model.generate_content(["Can you extract the grades in the format like subject1:mark1/subject2:mark2", img])
# print(response.text)

pdf_dir = os.path.join(BASE_DIR, 'extract_data','test_transcripts')
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        print()
        print(filename)
        images = pdf_to_imgs(pdf_path)
        if len(images)>16:
            images = images[-16:]
        response = model.generate_content(["Can you extract the grades in the format like subject1:mark1/subject2:mark2"]+images)
        print(response.text)