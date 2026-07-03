import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Set the Tesseract command path if it's not in the PATH environment variable
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

# Base directory where the 'transcripts' folder is located
base_dir = './transcripts'

# Directory to save OCR results
ocr_results_dir = './OCR_results'
if not os.path.exists(ocr_results_dir):
    os.makedirs(ocr_results_dir)

# Iterate over each region's folder in the 'transcripts' directory
for region in os.listdir(base_dir):
    region_path = os.path.join(base_dir, region)
    # Ensure the OCR_results directory mirrors the transcripts directory structure
    region_ocr_path = os.path.join(ocr_results_dir, region)
    if not os.path.exists(region_ocr_path):
        os.makedirs(region_ocr_path)

    # Make sure it's a directory
    if os.path.isdir(region_path):
        print(f"Processing region: {region}")
        
        # Iterate over each PDF in the region's folder
        for pdf_file in os.listdir(region_path):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(region_path, pdf_file)
                print(f"Processing file: {pdf_file}")
                
                # Convert PDF to list of images
                images = convert_from_path(pdf_path)

                # Prepare a text file to save OCR results
                txt_filename = os.path.splitext(pdf_file)[0] + '.txt'
                txt_path = os.path.join(region_ocr_path, txt_filename)
                
                # Open the text file
                with open(txt_path, 'w') as txt_file:
                    # Iterate over each image (page) and apply OCR
                    for i, image in enumerate(images):
                        text = pytesseract.image_to_string(image)
                        print(f"Page {i+1} Text:\n{text}")
                        txt_file.write(f"Page {i+1} Text:\n{text}\n")
                print(f"Finished processing file: {pdf_file}")




# import os
# import pytesseract
# from pdf2image import convert_from_path
# from PIL import Image

# # Base directory where the 'transcripts' folder is located
# base_dir = './transcripts'

# # Iterate over each region's folder in the 'transcripts' directory
# for region in os.listdir(base_dir):
#     region_path = os.path.join(base_dir, region)
    
#     # Make sure it's a directory
#     if os.path.isdir(region_path):
#         print(f"Processing region: {region}")
        
#         # Iterate over each PDF in the region's folder
#         for pdf_file in os.listdir(region_path):
#             if pdf_file.endswith('.pdf'):
#                 pdf_path = os.path.join(region_path, pdf_file)
#                 print(f"Processing file: {pdf_file}")
                
#                 # Convert PDF to list of images
#                 images = convert_from_path(pdf_path)

#                 # Iterate over each image (page) and apply OCR
#                 for i, image in enumerate(images):
#                     text = pytesseract.image_to_string(image)
#                     print(f"Page {i+1} Text:\n{text}")
