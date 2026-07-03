from core.models import *
from core.utility.update_data import *
from django.core.management.base import BaseCommand
import os
from datetime import datetime
import csv
import pandas as pd
from django.apps import apps
from core.utility import table_extractor


def load_data(file_path, db):
    # Implement your logic to load data into the database here
    # For example, you can use the csv module or a library like pandas
    match file_path.split('.')[-1]:
        case 'xlsl':
            # Read the Excel file into a DataFrame
            df_excel = pd.read_excel(file_path)
            # Get the column (title) names
            titles = df_excel.columns.tolist()

        case 'csv':
            # Read the CSV file into a DataFrame
            df_csv = pd.read_csv(file_path)
            # Get the column (title) names
            titles = df_csv.columns.tolist()
            res = db.load_data_from_file(df_csv)
            # Print the count of objects in the Tas_scaling model
            if res:
                print(f"Data loaded successfully. Total objects: {db.objects.all().count()}")
            else:
                print("Failed to load data.")
    pass


class Command(BaseCommand):
    help = 'Load CSV data into the database if the file has been modified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--model', type=str)

    def handle(self, *args, **options):
        csv_file_path = options['path']  # Replace with the actual path to your CSV file
        model_name = options['model']
        model_class = None
        if model_name == 'wa_language':
            table_extractor.wa_language_enter()
            return

        try:
            # Get the model class for the specified model name
            model_class = apps.get_model(app_label='core', model_name=model_name)

            # Now you can use the model_class as you need
            # For example, to retrieve all records from the table:
            table_data = model_class.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Retrieved data from {model_name}'))

        except LookupError:
            # Handle the case where the model with the given name does not exist
            self.stdout.write(self.style.ERROR(f"Model '{model_name}' does not exist."))
        if model_class:
            match model_name:
                case 'Subject':
                    initial_subject_from_excel()
                case 'Tas_scaling':
                    load_data(csv_file_path, model_class)
                case 'Region':
                    initial_region_from_excel()
                case 'GradeType':
                    initial_grade_type()
                case 'Wa_scaling':
                    table_extractor.extract_info('WA Scaling Table', csv_file_path)
                case 'Wa_atar':
                    table_extractor.extract_info('WA ATAR Table', csv_file_path)
                case 'Sa_atar':
                    table_extractor.extract_info('SA ATAR Table', csv_file_path)
                case 'Vic_scaling':
                    table_extractor.extract_info('VIC Scaling Table', csv_file_path)
                case 'Vic_atar':
                    table_extractor.extract_info('VIC ATAR Table', csv_file_path)