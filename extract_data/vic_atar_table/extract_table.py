# from pdfminer.high_level import extract_text

# # Specify the path to the PDF file
# pdf_file = './vic_atar.pdf'
# # Specify the output path for the txt file
# txt_file = './vic_atar.txt'

# # Extract text from the PDF file and save it to a txt file
# text = extract_text(pdf_file)
# with open(txt_file, 'w') as f:
#     f.write(text)


# import csv
# import re  # Import the regular expression module

# # List of words to remove
# words_to_remove = {"Small", "Study", "or", "no", "candidates,", "see", "Note", "below"}

# # Open the txt file
# with open('vic_scaling.txt', 'r') as txtfile:
#     # Read each line of the txt file
#     lines = txtfile.readlines()

#     # Open a new csv file, ready to write the converted data
#     with open('vic_scaling.csv', 'w', newline='') as csvfile:
#         # Create a csv writer
#         csvwriter = csv.writer(csvfile)

#         # Iterate through each line of the txt file
#         for line in lines:
#             # Use regular expression to split the string, \s+ matches one or more whitespace characters
#             data = re.split(r'\s+', line.strip())

#             # Check if the data contains any of the words to remove
#             if any(word in data for word in words_to_remove):
#                 # Remove specific words
#                 data = [word for word in data if word not in words_to_remove]
#                 # Add specified content at the end of the line
#                 data.extend(['24', '30', '35', '40', '44', '48', '51', 'small LOTEs'])

#             # Add an empty string at the end of each line of data as the default value for the 'category' column
#             data.append('')
#             # Write the data to the csv file
#             csvwriter.writerow(data)


import csv
import re  # Import the regular expression module

# Open the txt file
with open('vic_atar.txt', 'r') as txtfile:
    # Read each line of the txt file
    lines = txtfile.readlines()

    # Open a new csv file, ready to write the converted data
    with open('vic_atar.csv', 'w', newline='') as csvfile:
        # Create a csv writer
        csvwriter = csv.writer(csvfile)

        # Iterate through each line of the txt file
        for line in lines:
            # Use regular expression to split the string, \s+ matches one or more whitespace characters
            data = re.split(r'\s+', line.strip())
            # Write the data to the csv file
            csvwriter.writerow(data)
