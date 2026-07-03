import os
import pytesseract
import random
import string
import re
from pdf2image import convert_from_path

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_mapping_and_process_files(base_dir, ocr_results_dir):
    """Create a mapping of original file names to random strings and process the files."""
    mapping = {}
    
    for region in os.listdir(base_dir):
        region_path = os.path.join(base_dir, region)
        region_ocr_path = os.path.join(ocr_results_dir, region)
        if not os.path.exists(region_ocr_path):
            os.makedirs(region_ocr_path)

        if os.path.isdir(region_path):
            for pdf_file in os.listdir(region_path):
                if pdf_file.endswith('.pdf'):
                    pdf_path = os.path.join(region_path, pdf_file)
                    images = convert_from_path(pdf_path)
                    
                    # Generate a random string and create a mapping
                    random_str = generate_random_string()
                    mapping[pdf_file] = random_str
                    txt_path = os.path.join(region_ocr_path, f'{random_str}.txt')

                    with open(txt_path, 'w') as txt_file:
                        for image in images:
                            text = pytesseract.image_to_string(image)

                            # Make replacements case-insensitive
                            safe_text = text
                            for part in re.split(r'\W+', pdf_file.split('.')[0]):
                                if part.isalpha():
                                    pattern = re.compile(re.escape(part), re.IGNORECASE)
                                    safe_text = pattern.sub('[Confidential]', safe_text)
                                    
                            txt_file.write(safe_text)
                            # # Replace occurrences of the file name
                            # safe_text = text
                            # for part in re.split(r'\W+', pdf_file.split('.')[0]):
                            #     if part.isalpha():
                            #         safe_text = safe_text.replace(part, '[Confidential]')
                            # txt_file.write(safe_text)
    
    # Save the mapping table
    with open(os.path.join(ocr_results_dir, 'student_name_mapping3.txt'), 'w') as map_file:
        for pdf, rnd_str in mapping.items():
            map_file.write(f"{pdf} -> {rnd_str}\n")

# Set directory paths
base_dir = './transcripts'
ocr_results_dir = './OCR_results_confidential3'
if not os.path.exists(ocr_results_dir):
    os.makedirs(ocr_results_dir)

create_mapping_and_process_files(base_dir, ocr_results_dir)


# import os
# import pytesseract
# import random
# import string
# from pdf2image import convert_from_path

# def generate_random_string(length=10):
#     """Generate a random string of fixed length."""
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# def create_mapping_and_process_files(base_dir, ocr_results_dir):
#     """Create a mapping of original file names to random strings and process the files."""
#     mapping = {}
    
#     for region in os.listdir(base_dir):
#         region_path = os.path.join(base_dir, region)
#         region_ocr_path = os.path.join(ocr_results_dir, region)
#         if not os.path.exists(region_ocr_path):
#             os.makedirs(region_ocr_path)

#         if os.path.isdir(region_path):
#             for pdf_file in os.listdir(region_path):
#                 if pdf_file.endswith('.pdf'):
#                     pdf_path = os.path.join(region_path, pdf_file)
#                     images = convert_from_path(pdf_path)
                    
#                     # Generate a random string and create a mapping
#                     random_str = generate_random_string()
#                     mapping[pdf_file] = random_str
#                     txt_path = os.path.join(region_ocr_path, f'{random_str}.txt')

#                     with open(txt_path, 'w') as txt_file:
#                         for image in images:
#                             text = pytesseract.image_to_string(image)
#                             # Replace occurrences of the file name
#                             safe_text = text.replace(pdf_file.split('.')[0], '[Confidential]')
#                             txt_file.write(safe_text)
    
#     # Save the mapping table
#     with open(os.path.join(ocr_results_dir, 'student_name_mapping2.txt'), 'w') as map_file:
#         for pdf, rnd_str in mapping.items():
#             map_file.write(f"{pdf} -> {rnd_str}\n")

# # Set directory paths
# base_dir = './transcripts'
# ocr_results_dir = './OCR_results_confidential2'
# if not os.path.exists(ocr_results_dir):
#     os.makedirs(ocr_results_dir)

# create_mapping_and_process_files(base_dir, ocr_results_dir)
