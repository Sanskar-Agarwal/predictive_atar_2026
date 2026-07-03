from core.models import *
import os
import pandas as pd
from django.conf import settings


## update the subject, basic subject with subject.xlsx file if the table is empty
def initial_subject_from_excel():
    import_excel_to_model()


def initial_region_from_excel():
    if Region.objects.count() != 8:
        Region.objects.all().delete()
        region = ["New South Wales", "Victoria", "International Baccalaureate", "Queensland", "Tasmania",
                  "Western Australia", "Australian Capital Territory", "South Australia"]

        region_abbr = ['NSW', 'VIC', 'IB', 'QLD', 'TAS', 'WA', 'ACT', 'SA']
        for abbr, name in zip(region_abbr, region):
            reg = Region(name=name, abbreviation=abbr)
            reg.save()


def initial_grade_type():
    if GradeType.objects.count != 12:
        GradeType.objects.all().delete()
        des = ["1:Single numeric mark", "2:Single (A,B,C,D,E) grade", "3:Single (O,H,S,B,L) grade",
               "4:Multi categorical n=5 grades",
               "5:Multi categorical n < 5 grades", "6:Multi numeric weighted marks", "7:SACE single (A+ → E-) grade",
               "8:SACE multi (A+ → E-) weighted grade",
               "9:TAS year and final grade", "10:IB", "11:ACT", "12:Mixed numerical and categorical marks (QLD)"]
        label = ["numeric","categorical A,B,C,D,E","categorical O,H,S,B,L","categorical n=5","categorical n < 5","numeric weighted","SACE","SACE weighted","TAS year","IB","ACT","QLD"]
        for i in range(len(des)):
            gradetype = GradeType(description=des[i], label=label[i])

            gradetype.save()


"""" this file is used to upload the excel file into our database, the subjects are loaded by this file functions"""


def import_excel_to_model():
    ## delete all the items in the subject and basicsubject
    Subject.objects.all().delete()
    BasicSubject.objects.all().delete()
    # Read the Excel file into a DataFrame
    project_dir = os.getcwd()

    file_path = os.path.join(project_dir, "core/source/subjects.xlsx")

    region_abbr = ['NSW', 'VIC', 'IB', 'QLD', 'TAS', 'WA', 'ACT', 'SA']
    for i in region_abbr:
        basic_df = pd.read_excel(file_path, sheet_name=i + '_basic')  # Specify the sheet name
        all_df = pd.read_excel(file_path, sheet_name=i + '_all')

        # Iterate through rows in the DataFrame and create YourModel instances
        try:
            temp = Region.objects.filter(abbreviation=i)
            region = temp.first()
        except:
            raise CustomErrorException(" can not find the region id via abbreviation")
        for i, r in all_df.iterrows():
            created_subject = Subject.objects.create(
                subject=r['Subject'],
                units=r['Units'],
                category=r['Category'],
                regionid=region,
            )

            ## check if it is exist in anywhere of the df
            is_a_basic = basic_df.isin([created_subject.subject])

            if is_a_basic.values.any():
                # Check if the value is present in any column, and get the column names
                columns_with_value = is_a_basic.columns[is_a_basic.any()].tolist()
                name_of_title = columns_with_value[0]
                ## create
                BasicSubject.objects.create(
                    title=name_of_title,
                    regionid=region,
                    subjectid=created_subject
                )
