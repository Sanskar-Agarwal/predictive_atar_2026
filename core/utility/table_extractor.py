import pandas as pd
import pdfplumber
import tabula
import os
import django
from core.models import *
import numpy as np  # Used for detecting NaN values

def extract_info(document_type, file_path):
    if document_type == "NSW Scaling Table":
        nsw_atar_data_df = pd.DataFrame()
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                # As table is over multiple pages
                nsw_atar_data_df = pd.concat([nsw_atar_data_df, pd.DataFrame(table[1:], columns=table[0])])
                nsw_atar_data_df = nsw_atar_data_df.reset_index(drop=True)
        print(nsw_atar_data_df.index.max())
        Nsw_scaling.objects.all().delete()
        for index, row in nsw_atar_data_df.iterrows():
            #print(index)
            course = row.iloc[0] if row.iloc[0] else course
            number = int(row.iloc[1].replace(',', '')) if row.iloc[1] else number
            instance = Nsw_scaling(
            course = course,
            number = number,
            type_of_mark = row.iloc[2],
            mean = float(row.iloc[3]) if row.iloc[3].strip() else 0,
            sd = float(row.iloc[4]) if row.iloc[4].strip() else 0,
            max_mark = float(row.iloc[5]) if row.iloc[5].strip() else 0,
            p99 = float(row.iloc[6]) if row.iloc[6].strip() else 0,
            p90 = float(row.iloc[7]) if row.iloc[7].strip() else 0,
            p75 = float(row.iloc[8]) if row.iloc[8].strip() else 0,
            p50 = float(row.iloc[9]) if row.iloc[9].strip() else 0,
            p25 = float(row.iloc[10]) if row.iloc[10].strip() else 0)
            instance.save()
            if(index == 0):
                for index1, value in row.items():
                    index1 = index1.replace("\n", "")
                    index1 = index1.replace("\r\n", "")
                    index1 = index1.replace(" ", "")
                    print(f"Index: {index1}")
                    #print(f"Index: {index1}, Value: {value}")

    elif default_group_counter == "NSW ATAR Conversion Table":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    topLeftCell = table[1][0]
                    years = []
                    if(topLeftCell=='ATAR'):
                        num_rows = len(table)
                        num_columns = len(table[0]) if num_rows > 0 else 0
                        Nsw_atar.objects.all().delete()
                        for x in range(1,num_columns):
                            years.append(table[1][x])
                        for row in range(2, num_rows):
                            for col in range(1, num_columns):
                                instance = Nsw_atar(
                                    atar = table[row][0],
                                    year = table[1][col],
                                    score = table[row][col]
                                )
                                instance.save()
    elif default_group_counter == "WA Scaling Table":
        dfs = [df for df in tabula.read_pdf(file_path, pages='all')]
        new_df = pd.concat(dfs, axis=0)
        Wa_scaling.objects.all().delete()
        for _, row in new_df.iterrows():
            if(row.iloc[1].replace(',', '').isdigit()):
                instance = Wa_scaling(
                course = row.iloc[0],
                mean = float(row.iloc[2]) if not pd.isna(row.iloc[2]) else 0,
                min_mark = float(row.iloc[4]) if not pd.isna(row.iloc[4]) else 0,
                max_mark = float(row.iloc[5]) if not pd.isna(row.iloc[5]) else 0
                )
                instance.save()
    elif default_group_counter == "WA ATAR Table":
        df = pd.read_excel(file_path)
        Wa_atar.objects.all().delete()
        for _, row in df.iterrows():
            instance = Wa_atar(
                atar = row.iloc[0],
                min_tea = row.iloc[1]
            )
            instance.save()
    elif default_group_counter == "SA ATAR Table":
        dfs = [df for df in tabula.read_pdf(file_path, pages='all')]
        Sa_atar.objects.all().delete()
        new_df = pd.concat(dfs, axis=0)
        for _, row in new_df.iterrows():
            instance = Sa_atar(
                aggregate = row.iloc[0],
                atar = row.iloc[1]
            )
            instance.save()
    elif default_group_counter == "TAS ATAR Table":
        csv_path = '/Users/QIan/PycharmProjects/atarcalc_new/venv/predicative_atar/core/source/atar_csv/atar_tas.csv'
        #df = tabula.read_pdf(file_path, pages='all', lattice=True)
        #table_df = df[0]
         #table_df.to_csv(csv_path, index=False)
        df = pd.read_csv(csv_path)
        reshaped_df = pd.DataFrame({
                'TE Score': df.iloc[:, ::2].values.flatten(),
                'ATAR': df.iloc[:, 1::2].values.flatten()
            })
        reshaped_df['TE Score'] = pd.to_numeric(reshaped_df['TE Score'], errors='coerce')
        reshaped_df = reshaped_df.sort_values(by='TE Score', ascending=False)
        reshaped_df.to_csv(csv_path, index=False)

        Tas_atar.objects.all().delete()
        for _, row in reshaped_df.iterrows():
            instance = Tas_atar(
                tes=row['TE Score'],
                atar=row['ATAR']
            )
            instance.save()
    elif default_group_counter == "TAS Scaling Table":
        csv_path = '/Users/QIan/PycharmProjects/atarcalc_new/venv/predicative_atar/core/source/scaling_csv/tas_scaling.csv'
        csv_path = file_path
        Tas_scaling_alt.objects.all().delete()
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            instance = Tas_scaling_alt(
                course = row['COURSE'],
                sa_min = row['SA_Min'],
                sa_max = row['SA_Max'],
                ca_min = row['CA_Min'],
                ca_max = row['CA_Max'],
                ha_min = row['HA_Min'],
                ha_max = row['HA_Max'],
                ea_min = row['EA_Min'],
                ea_max = row['EA_Max']
            )
            instance.save(  )
    elif default_group_counter == "VIC Scaling Table":
        # csv_path = '/Users/cccurie/Desktop/predicative_atar/core/source/scaling_csv/vic_scaling.csv'
        csv_path = file_path
        Vic_scaling.objects.all().delete()
        df = pd.read_csv(csv_path)
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Create a Vic_scaling instance, checking for NaN values and replacing them with None
            instance = Vic_scaling(
                study_code=row['study_code'],  # Assuming 'study_code' is always valid
                study_name=row['study_name'],  # Assuming 'study_name' is always valid
                mean=None if pd.isna(row['mean']) else row['mean'],  # Replace NaN with None for 'mean'
                sd=None if pd.isna(row['sd']) else row['sd'],  # Replace NaN with None for 'sd'
                scaled_score_20=None if pd.isna(row['scaled_score_20']) else row['scaled_score_20'],  # Replace NaN with None
                scaled_score_25=None if pd.isna(row['scaled_score_25']) else row['scaled_score_25'],  # Replace NaN with None
                scaled_score_30=None if pd.isna(row['scaled_score_30']) else row['scaled_score_30'],  # Replace NaN with None
                scaled_score_35=None if pd.isna(row['scaled_score_35']) else row['scaled_score_35'],  # Replace NaN with None
                scaled_score_40=None if pd.isna(row['scaled_score_40']) else row['scaled_score_40'],  # Replace NaN with None
                scaled_score_45=None if pd.isna(row['scaled_score_45']) else row['scaled_score_45'],  # Replace NaN with None
                scaled_score_50=None if pd.isna(row['scaled_score_50']) else row['scaled_score_50'],  # Replace NaN with None
                category=None if pd.isna(row['category']) else row['category'],  # Replace NaN with None for 'category'
                group=None if pd.isna(row['group']) else row['group']  # Replace NaN with None for 'category'
            )
            instance.save()
    elif default_group_counter == "VIC ATAR Table":
        # csv_path = '/Users/cccurie/Desktop/predicative_atar/core/source/atar_csv/vic_atar.csv'
        csv_path = file_path
        Vic_atar.objects.all().delete()  # Clear existing entries to avoid duplicates
        df = pd.read_csv(csv_path)
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Create a Vic_atar instance, checking for NaN values and replacing them with None
            instance = Vic_atar(
                atar=None if pd.isna(row['atar']) else row['atar'],  # Replace NaN with None for 'atar'
                range_low=None if pd.isna(row['range_low']) else row['range_low'],  # Replace NaN with None for 'range_low'
                range_high=None if pd.isna(row['range_high']) else row['range_high']  # Replace NaN with None for 'range_high'
            )
            instance.save()   




def wa_language_enter():
    wa_language_list = ['Aboriginal and Intercultural Studies: Aboriginal Languages', 'Arabic', 'Armenian',
                     'Auslan (Australian Sign Language)', 'Bengali', 'Bosnian', 'Chin Hakha',
                     'Chinese: Background Language', 'Chinese: First Language', 'Chinese: Second Language', 'Croatian',
                     'Dutch', 'Filipino', 'French: Background Language', 'French: Second Language',
                     'German: Background Language', 'German: Second Language', 'Hebrew', 'Hindi: Background Language',
                     'Hindi: Second Language', 'Hungarian', 'Indonesian: First Language', 'Indonesian: Second Language',
                     'Italian: Background Language', 'Italian: Second Language', 'Japanese: Background Language',
                     'Japanese: Second Language', 'Karen', 'Khmer', 'Korean: Background Language',
                     'Korean: Second Language', 'Macedonian', 'Malay: Background Speakers', 'Modern Greek', 'Nepali',
                     'Persian', 'Punjabi', 'Romanian', 'Russian', 'Serbian', 'Sinhala', 'Spanish', 'Swedish',
                     'Tamil: Background Language', 'Turkish',
                     'Vietnamese']
    for subject in wa_language_list:
        Subject.objects.filter(subject=subject,regionid=6).update(is_language=True)

def main():
    # Your main code goes here
    #print("Current working directory:", os.getcwd())
    #extract_info('NSW Scaling Table', './core/source/scaling_pdf/nsw_scaling.pdf')
    extract_info('NSW ATAR Conversion Table', './core/source/atar_pdf/nsw_atar.pdf')

if __name__ == "__main__":
    main()

