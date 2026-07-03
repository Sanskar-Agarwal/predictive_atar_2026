from collections import defaultdict

import numpy
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from core.models import *
from core.utility.tools import *
from core.utility.atar_calculate_main import *
from core.utility.atar_calculate_vic import *
from django.db import transaction
from core.serializer import *
import logging
import json
from core.utility.mark_convert import *

from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.views.decorators.csrf import csrf_exempt

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.views.decorators.csrf import csrf_exempt

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from core.utility.HighestMathLevel import find_highest_math
import datetime
import pytz


# temp
from core.utility.table_extractor import *

logger = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Every submission row is appended to each of these spreadsheets. Each one must
# be shared (Editor) with the service account in credentials.json.
SPREADSHEET_IDS = [
    '1ROvCcwdTT6NIut97ZBSf9Fb_Zch9YR4vvI0Hbd_ts1E',
    '1KXYP5lLlojTfY8Z4eZ0uM7HY7g_BDNFqN35uN-2kIdg',
]


def send_sheets_request(data):

    sheet_range = 'Sheet1'

    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )

    # Append the timestamp once so the same row is written to every sheet.
    utc_datetime = datetime.datetime.utcnow()
    aest = pytz.timezone('Australia/Sydney')
    aest_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(aest)
    data.append(aest_datetime.strftime("%m/%d/%Y, %H:%M:%S"))

    service = build("sheets", "v4", credentials=credentials)
    body = {"values": [data]}

    results = []
    for spreadsheet_id in SPREADSHEET_IDS:
        try:
            result = (
                service.spreadsheets()
                    .values()
                    .append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_range,
                    valueInputOption='USER_ENTERED',
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended to {spreadsheet_id}.")
            results.append(result)
        except HttpError as error:
            # Don't let one failing sheet stop the others (e.g. not shared yet).
            print(f"An error occurred writing to {spreadsheet_id}: {error}")
            results.append(error)
    return results






"""this function search all the subject grouped by the basic subject by region id"""


@handle_errors
def select_subject_by_region(request):
    try:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                region_abbreviation = data.get('region_abbr').upper()
                # this part only check the region exist in current db table Region
                region_objects = Region.objects.filter(abbreviation=region_abbreviation)

                if region_objects.count() != 1:
                    raise CustomErrorException("cannot find the region")
                # Get all basic subjects for the given region
                basic_subjects = BasicSubject.objects.filter(regionid__abbreviation=region_abbreviation)
                # Create a dictionary to store subjects grouped by basic subject
                subjects_grouped_by_basic = {}
                # find the subject by the region's abbreviation
                subjects_in_region = Subject.objects.filter(regionid__abbreviation=region_abbreviation)

                # Group subjects by basic subject
                for basic_subject in basic_subjects:
                    basic_subject_title = basic_subject.title
                    subjects_for_basic_subject = subjects_in_region.filter(subject=basic_subject.subjectid.subject)
                    subjects_for_basic_subject_list = list(subjects_for_basic_subject.values())
                    if basic_subject_title in subjects_grouped_by_basic:
                        subjects_grouped_by_basic[basic_subject_title].extend(subjects_for_basic_subject_list)
                    else:
                        subjects_grouped_by_basic[basic_subject_title] = subjects_for_basic_subject_list
                # Find subjects not in basic subjects and add them to the "other" category
                subjects_not_in_basic = subjects_in_region.exclude(
                    id__in=BasicSubject.objects.filter(regionid__abbreviation=region_abbreviation).values('subjectid'))

                subjects_grouped_by_basic['Other'] = list(subjects_not_in_basic.values())

                return JsonResponse(subjects_grouped_by_basic, safe=False)
            except json.JSONDecodeError as e:
                raise CustomErrorException(e)
    except CustomErrorException as e:
        logger.error(f"CustomErrorException: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)  ## bad request defined by ourself

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


"""this function calculates the atar score and store it to the database, it will be use in the next function 
select_subjects_and_grades which is the api that calculate the final atar 
"""


@handle_errors
def storage_student_score(score, region_abbr, appid, name, note):
    try:
        with transaction.atomic():
            atar = 0  ## remove it once the final option is done
            auto_note = ""  # set by a region calc when it needs to flag something (e.g. NSW <10 units)

            region_names = Region.objects.filter(abbreviation=region_abbr)

            if not region_names:
                raise CustomErrorException("cannot find the abbreviation of region name, try again")
            region_abbreviation = region_names.first().abbreviation
            ## query the subject and unit in Subject table
            subjects_and_units = Subject.objects.filter(subject__in=score.keys(),
                                                        regionid__abbreviation=region_abbreviation).values('subject',
                                                                                                           'units')

            ## convert it into dic format
            subjects_and_units_dict = {subject['subject']: int(subject['units']) for subject in subjects_and_units}

            # Create a new dictionary {subject: (mark, unit)}
            if region_abbreviation == 'IB':
                subjects = convert_ib(score)
                combined_dict = {subject: (mark, subjects_and_units_dict.get(subject)) for subject, mark in
                                 subjects.items()}
            else:
                combined_dict = {subject: (mark, subjects_and_units_dict.get(subject)) for subject, mark in
                                 score.items()}

            # A subject not found in the Subject table above silently ends up here
            # with unit=None. Left unchecked, that None reaches each region's own
            # calculation code (e.g. NSW's float(unit) in nsw_scaling), which
            # crashes with a generic TypeError that storage_student_score's outer
            # except-Exception swallows into a confusing "'NoneType' object has no
            # attribute 'tolist'" 500 error — instead of naming the actual subject.
            # Catch it here, once, for every region that actually uses combined_dict
            # AND relies on "unit" meaning something.
            # TAS is excluded: its combined_dict here is keyed by year (e.g. 2026),
            # not by subject name — tas_calculation uses `score` directly instead
            # (see below) — so checking combined_dict for TAS is checking garbage
            # and previously crashed on year (an int) where a subject name (str)
            # was expected. TAS's own subject-name validation already happens
            # earlier, inside convert_cat_tas.
            # IB is excluded too: ib_calculation only ever sums the mark half of
            # each (mark, unit) tuple, never the unit — and convert_ib always adds
            # a synthetic 'ToKEE' bonus-points entry that is never a real Subject
            # row, so this check would reject every single IB submission on that
            # entry alone.
            if region_abbreviation not in ('TAS', 'IB'):
                unmatched_subjects = [subject for subject, (_, unit) in combined_dict.items() if unit is None]
                if unmatched_subjects:
                    raise CustomErrorException(
                        f"Subject(s) not recognised for {region_abbreviation}: {', '.join(unmatched_subjects)}. "
                        "Please check the subject name."
                    )

            if region_abbreviation == "NSW":
                atar, auto_note = nsw_calculation(combined_dict)
            elif region_abbreviation == "VIC":
                atar = vic_calculation(combined_dict)
            elif region_abbreviation == "WA":
                atar = wa_calculate(combined_dict)
            elif region_abbreviation == "ACT":
                atar = act_calculation(combined_dict)
            elif region_abbreviation == "IB":
                atar = ib_calculation(combined_dict)
            elif region_abbreviation == "TAS":
                atar = tas_calculation(score)
            elif region_abbreviation == "SA":
                atar = sace_calculate(combined_dict)
            elif region_abbreviation == "QLD":
                atar = qld_calculation(combined_dict)

            # fold any auto-generated note (e.g. NSW <10 units) into the note so it
            # is stored on the record and logged to the sheet. Guard against
            # re-appending if the note already carries it (e.g. on a resubmit).
            note = note or ""
            if auto_note and auto_note not in note:
                note = f"{note} | {auto_note}".strip(" |")

            # search the applicant exist or not
            applicant = ApplicationStudent.objects.filter(applicantionid=appid).first()
            ## if it is exist just update it.

            if applicant != None:
                applicant.delete()

            new_application = ApplicationStudent.objects.create(applicantionid=appid, regionid=region_names.first().id,
                                                                atar=atar, name=name, note=note)


            if region_abbr == 'TAS':
                temp = []
                temp1 = []
                # print(list(score.items()))
                for item in score.items():
                    temp.append(list(item[1].items()))
                for item in temp:
                    for i in range(1, len(item[0]), 1):
                        temp1.append(item[0][i])
                temp = []
                for item in temp1:
                    for x in item:
                        temp.append(x)
                try:
                    data_for_math = []
                    for item in temp:
                        # print('itemsubject: ', item['subject'])
                        data_for_math.append(item['subject'])
                        subject = Subject.objects.get(regionid__id=region_names.first().id, subject=item['subject'])
                        ApplicationStudentSubject.objects.create(application_student=new_application, subject=subject,
                                                                marks=item['score'])

                    highest_math = find_highest_math(data_for_math, 'TAS')
                    # print('highest_math: ', highest_math)
                except Subject.DoesNotExist:
                    traceback.print_exc()
                    raise CustomErrorException(
                        f"Subject with region name {region_names.first().name} and subject name {subject} does not exist.")
                except CustomErrorException as e:
                    traceback.print_exc()
                    raise CustomErrorException(f"the error happened in the database, please check the storage: {e}")

                data = [
                    appid,
                    name,
                    float(atar),
                    region_abbr,
                    note,
                    highest_math
                ]
                try:
                    send_sheets_request(data)
                except Exception as e:
                    # The ATAR (float(atar) above) was already computed
                    # successfully at this point — a Sheets-logging failure
                    # (missing credentials.json, network, quota, permissions)
                    # used to fall through to the outer bare except and surface
                    # as a confusing "'NoneType' object has no attribute
                    # 'tolist'" 500, discarding a good result.
                    traceback.print_exc()
                    raise CustomErrorException(f"Calculated the ATAR but failed to log it to Google Sheets: {e}")
                return float(atar), auto_note
            else:
                data_for_math = []
                for subject_name, mark in score.items():
                    try:
                        data_for_math.append(subject_name)
                        subject = Subject.objects.get(regionid__id=region_names.first().id, subject=subject_name)
                        # add the subject into the list
                        ApplicationStudentSubject.objects.create(application_student=new_application, subject=subject,
                                                                 marks=mark)
                    except Subject.DoesNotExist:
                        traceback.print_exc()
                        raise CustomErrorException(
                            f"Subject with region name {region_names.first().name} and subject name {subject_name} does not exist.")
                    except CustomErrorException as e:
                        traceback.print_exc()
                        raise CustomErrorException(f"the error happened in the database, please check the storage: {e}" )
                highest_math = find_highest_math(data_for_math, region_abbr)
                # print('highest_math: ', highest_math)
                data = [
                    appid,
                    name,
                    float(atar),
                    region_abbr,
                    note,
                    highest_math
                ]
                try:
                    send_sheets_request(data)
                except Exception as e:
                    traceback.print_exc()
                    raise CustomErrorException(f"Calculated the ATAR but failed to log it to Google Sheets: {e}")
                return atar, auto_note

    except CustomErrorException as e:
        traceback.print_exc()
        return {'error': str(e)}
    except Exception as e:
        traceback.print_exc()
        #  Handle any other exceptions
        print(f"An error occurred: {str(e)}")
        # Optionally, you can log the error or perform additional error handling
        #  Rollback the transaction
        # transaction.set_rollback(True)


@handle_errors
def get_grade_type_decription(request):
    try:
        label = request.GET.get('label', '')
        data_object = get_object_or_404(GradeType, label=label)
        serializer = GradeTypeSerializer(data_object)

        # Check if the serializer is a DRF serializer
        if isinstance(serializer, serializers.Serializer):
            serialized_data = serializer.data  # Use .data for DRF serializers
        else:
            serialized_data = serializer  # Use serializer directly if not a DRF serializer

        return JsonResponse(serialized_data)

    except CustomErrorException as e:
        logger.error(f"CustomErrorException: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)  ## bad request defined by ourself

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


# @handle_errors
# def select_basic_subject_and_subject_by_region(request):
#     try:
#         if request.method == 'POST':
#
#             region = request.POST.get("region")
#
#             region_id = Region.get_id_by_abbreviation(region)
#             if not region_id:
#                 raise CustomErrorException("cannot find the region")
#
#             basic_subjects = BasicSubject.objects.filter(regionid=region_id)
#             subjects_dict = defaultdict(list)
#
#             # Collect subjects from BasicSubject model
#             for basic_subject in basic_subjects:
#                 subjects_dict[basic_subject.title].append(basic_subject.subjectid.subject)
#
#             # Collect subjects from Subject model that belong to the specified region but not in BasicSubject
#             other_subjects = Subject.objects.filter(regionid=region_id).exclude(
#                 id__in=basic_subjects.values('subjectid__id'))
#             for other_subject in other_subjects:
#                 subjects_dict['Other'].append(other_subject.subject)
#             return JsonResponse(subjects_dict)
#
#     except CustomErrorException as e:
#         logger.error(f"CustomErrorException: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=400)  ## bad request defined by ourself
#
#     except Exception as e:
#         # Handle other exceptions
#         return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


@handle_errors
def select_subjects_and_grades(request):
    try:
        if request.method == 'POST':

            raw_data = request.body.decode('utf-8')

            try:
                # Load the raw data into a Python dictionary
                data = json.loads(raw_data)

                # Extract values from the dictionary
                region_id = data.get("region_abbr")
                app_id = data.get("application_id")
                grade_type = data.get("grade_type")
                subjects = data.get("subjects", {}).get(grade_type, {})
                name = data.get("applicant_name")
                note = data.get("note")
                # the data structure of subjects is {"English":{mark:77,max_mark:100},"Math":{mark:88,max_mark:100}}
                ## for detail please see the readme inside the frontend
                if grade_type == "Numerical": 
                    subjects = convert_json_dictionary(
                                subjects
                    )  ## the structure should be like this {"English":88,"Math":90}
                elif grade_type == "ABCDE":
                    subjects = convert_json_dictionary(subjects)
                    subjects = convert_categorical(subjects, True)

                elif grade_type == "OHSBL":
                    subjects = convert_json_dictionary(subjects)
                    subjects = convert_categorical(subjects, False)

                elif grade_type == "Numerical Weighted":
                    subjects = convert_weighted_num(subjects)

                elif grade_type == "IB":
                    subjects = convert_json_dictionary(subjects)

                elif grade_type == "Numerical & Categorical":
                    subjects = convert_json_dictionary(subjects)
                    check_list = ['A', 'B', 'C', 'D', 'E']
                    categorical_dic = {}
                    numerical_dic = {}
                    for sub, ma in subjects.items():
                        ## the sending is int for number and string for cate
                        if type(ma) in [int,float]:
                        #if ma.isnumeric():
                            numerical_dic[sub] = ma
                        elif ma.upper() in check_list:
                            categorical_dic[sub] = ma
                        else:
                            raise CustomErrorException(
                                str("undefined type of input, the subject %s and mark %s not correct", sub, ma))
                    temp = convert_categorical(categorical_dic, True)
                    numerical_dic.update(temp)
                    subjects = numerical_dic

                elif grade_type == "A+ to E-":
                    subjects = convert_json_dictionary(subjects)
                    subjects = convert_sa_single(subjects)

                elif grade_type == "A+ to E- With Weighted":
                    subjects = convert_sa_weighted_num(subjects)

                elif grade_type == "ACT Combined Weighted Category & Numerical":
                    subjects = convert_act(subjects)

                elif grade_type == "TAS Year":
                    # update_tas_subjects()
                    # extract_info('TAS Scaling Table', '/Users/QIan/PycharmProjects/atarcalc_new/venv/predicative_atar/core/source/scaling_csv/tas_scaling.csv')
                    # extract_info('TAS ATAR Table', '/Users/QIan/PycharmProjects/atarcalc_new/venv/predicative_atar/core/source/atar_csv/atar_tas.csv')
                    subjects = convert_cat_tas(subjects)
                    # print('subjects: ', subjects)

                elif grade_type == "Multiple Categorical Grade":
                    subjects = convert_multi_cat(subjects)
                res = storage_student_score(subjects, region_id, app_id, name, note)

            except json.JSONDecodeError as e:

                # Handle JSON decoding error
                raise CustomErrorException("json file error:" + str(e))

            # storage_student_score returns (atar, auto_note) on success; older
            # paths may still return a bare value, so unpack defensively.
            auto_note = ""
            if isinstance(res, tuple):
                res, auto_note = res

            if isinstance(res, (int, float, np.generic, Decimal)):
                return JsonResponse({"atar": float(res), "note": auto_note}, safe=False)

            # A region calc that hits a hard-block (e.g. NSW <10 units) returns an
            # {'error': message} dict — pass the message straight through so the UI
            # can show it (instead of crashing on res.tolist()).
            if isinstance(res, dict) and 'error' in res:
                return JsonResponse({'error': res['error']}, status=400)

            res = json.dumps(res.tolist())

            return JsonResponse({"atar": res})
    except CustomErrorException as e:
        logger.error(f"CustomErrorException: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)  ## bad request defined by ourself

    except Exception as e:
        # Handle other exceptions
        traceback.print_exc()
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

