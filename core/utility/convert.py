import csv

import tabula
import pandas as pd
import os




def convert_pdf_to_csv(pdf_path,csv_file_path):
    if os.path.exists(pdf_path):
        dfs = [df.set_index(df.columns[0]) for df in tabula.read_pdf(pdf_path, pages='all')]

        new_df = pd.concat(dfs, axis=0)
        new_df.reset_index(inplace=True)
        new_df.to_csv(csv_file_path, index=False)  # Save DataFrame to CSV file
        return new_df
    else:
        print("error")
        return



##check csv file with data cleaning
def check_csv_file(csv_file_path):
    match csv_file_path.split("/")[-1]:
        case "tas_scaling.csv":
            # Read CSV file skipping the first two rows
            print("solve the issue about tas_scaling file")
            df = pd.read_csv(csv_file_path, skiprows=[0, 1])

            # Set a new header row
            new_header = ['CODE', 'COURSE', 'NN/PA_N', 'SA_Min', 'SA_Max', 'SA_N', 'CA_Min', 'CA_Max', 'CA_N',
                              'HA_Min', 'HA_Max', 'HA_N', 'EA_Min',
                              'EA_Max', 'EA_N']
            df.columns = new_header
            code_pattern = r'^[A-Za-z]{3}\d{6}$'
            filtered_df = df[df['CODE'].str.match(code_pattern, na=False)]

            # Write the corrected data to a new CSV file
            filtered_df.to_csv(csv_file_path, index=False)
        case "nsw_scaling.csv":
            print('solve the issue about nsw_scaling file')
            df = pd.read_csv(csv_file_path, skiprows=[0, 1])
            df = df.dropna(axis=1, how='all')

            # Identify columns with missing data
            columns_with_missing_data = df.columns[df.isnull().any()]

            # Iterate over columns with missing data and fill missing values from the next column
            for col in columns_with_missing_data:
                df[col].fillna(df.shift(axis=1)[col], inplace=True)

            # Drop the unwanted columns (the ones with missing values)
            # df = df.dropna(axis=1)

            new_header = ['course','number','type of mark','mean','sd','max','p99','p90','p75','p50','p25']
            df.columns = new_header

    return




def convert_csv_to_database(csv_file_path,db):
    with open(csv_file_path, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # Assuming the first row contains column names

        for row in reader:
            model_kwargs = {}  # Dictionary to store attribute-value pairs

            for col_name, col_value in zip(header, row):
                model_kwargs[col_name] = col_value

            _, created = db.objects.get_or_create(**model_kwargs)

