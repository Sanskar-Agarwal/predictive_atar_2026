import json
from enum import Enum
from core.models import *

A_NUM = 92
B_NUM = 82
C_NUM = 72
D_NUM = 61
E_NUM = 37
NUM_GRADES = [A_NUM, B_NUM, C_NUM, D_NUM, E_NUM]

MULTI_CAT = {
    'outstanding': A_NUM,
    'high': B_NUM,
    'sound': C_NUM,
    'basic': D_NUM,
    'limited': E_NUM,
}
O_CAT = {
    'o': A_NUM,
    'h': B_NUM,
    's': C_NUM,
    'b': D_NUM,
    'l': E_NUM,
}

A_CAT = {
    'a': A_NUM,
    'b': B_NUM,
    'c': C_NUM,
    'd': D_NUM,
    'e': E_NUM,
}

TAS_CAT = {
    'ea': A_NUM,
    'ha': B_NUM,
    'ca': C_NUM,
    'sa': D_NUM,
    'pa': E_NUM,
    'nn': 0,
}


## convert front end data into readable backend data
## output {subject_name:mark,...}
## input : {math:{mark:A},english:{mark:88}}
def convert_json_dictionary(raw_marks):

    result = {}
    for subject, marks in raw_marks.items():
        try:
            if "max_mark" in marks:
                mark = (marks["mark"] / marks["max_mark"]) * 100
            else:
                mark = marks["mark"]
            result[subject] = mark
        except (KeyError, TypeError) as e:
            print(f"Error processing marks for subject '{subject}': {e}")
    print("the converted json to the backend list ",result)
    return result


# CONVERT CATEGORICAL - to numerical
# raw marks format: { subject_name : mark, ...}
# is_abcde: if true, calculates for ABCDE grading, if false, calculates for OHSBL grading
# returned format: { subject_name : converted_mark, ...}
def convert_categorical(raw_marks, is_abcde):
    converted_marks = {}

    subjects = list(raw_marks.keys())
    for subject in subjects:
        # extract the grade for the subject
        grade = raw_marks[subject][0].lower()

        # convert the grade and store in a new dictionary
        if is_abcde:
            converted_marks[subject] = A_CAT.get(grade)
        else:
            converted_marks[subject] = O_CAT.get(grade)

    return converted_marks


# CONVERT NUMERICAL - Weighted tasks per subject
# May need to create a method to convert raw marks format, depends on API
# Can also change format if needed.
# raw marks format:
# Assumptions: weighting is scaled 0 - 100 (i.e. 70 for 70% weighting)
#              mark is the mark obtained by the student on the assessment
#              max_mark is the maximum mark that can be obtained on the assessment
#              subject_name should only occur once per subject
#
# {
#     subject_name : {
#         subject_task : {
#              weighting : 70,
#              mark : 80
#              max_mark : 90
#         },
#         subject_task2 : {
#             weighting : 30,
#             mark : 50
#             max_mark : 10
#         }
#     },
#     subject_name2...
# }

# returned format: { subject_name : converted_mark, ...}

def convert_weighted_num(raw_marks):
    converted_marks = {}

    for subject, tasks in raw_marks.items():
        temp = 0
        total_weight = 0
        for task, details in tasks.items():
            total_weight += details['weighting']

        for task, details in tasks.items():
            temp += ((details['mark'] * 100) / details['max_mark']) * (details['weighting'] / total_weight)

        # Scale to 100 if total weight is less than 100
        # if total_weight < 100:
        #     scaling_factor = 100 / total_weight
        #     temp *= scaling_factor

        converted_marks[subject] = temp

    return converted_marks


def convert_sa_weighted_num(raw_marks):
    converted_marks = {}

    for subject, tasks in raw_marks.items():
        temp = 0
        total_weight = 0
        for task, details in tasks.items():
            total_weight += details['weighting']

        for task, details in tasks.items():
            temp += (convert_sa_individual(details['mark'].lower())) * (details['weighting'] / total_weight)

        # Scale to 100 if total weight is less than 100
        # if total_weight < 100:
        #     scaling_factor = 100 / total_weight
        #     temp *= scaling_factor

        converted_marks[subject] = temp

    return converted_marks


# CONVERT CATEGORICAL - Multiple grades per subject
# raw_marks format:
# {
#     subject_name : {
#         a : 1,
#         b : 1,
#         c : 0,
#         d : 1,
#         e : 2
#     },
#     ...
# }
# is_abcde: if true, calculates for ABCDE grading, if false, calculates for OHSBL grading
# Output format:
# { subject_name : converted_mark, ...}
def convert_multi_cat(raw_marks):
    converted_marks = {}
    for subject, grades in raw_marks.items():
        current_total = 0
        grade_count = 0
        grades = grades["marks"]
        for grade, count in grades.items():

            grade_count += count
            if not str(grade).isnumeric():
                current_total += MULTI_CAT[grade.lower()] * count

            else:
                current_total += float(grade) * count
            
        converted_marks[subject] = current_total / grade_count
        
    
    return converted_marks
## convert Multi categorical n=5
##
def convert_multi_ohsbl(raw_marks):
    converted_marks = {}
    for subject, grades in raw_marks.items():
        pass

    return

# Helper method for SA marks
def convert_sa_individual(raw):
    tempmark = 0
    for grade in A_CAT.keys():
        if grade in raw:
            tempmark = A_CAT[grade]
            break
    if '+' in raw:
        tempmark += 4
    elif '-' in raw:
        tempmark -= 4

    return tempmark


# CONVERT SA GRADES (A+, A, A-, etc.) to numerical
# raw_marks format:
# { subject_name : mark, ...}
# Output format:
# { subject_name : converted_mark, ...}
def convert_sa_single(raw_marks):
    converted_marks = {}
    for subject in raw_marks.keys():
        current = raw_marks[subject].lower()
        tempmark = convert_sa_individual(current)

        converted_marks[subject] = tempmark

    return converted_marks


# CONVERT SA WEIGHTED GRADES (A+, A, A-, etc.) to numerical
# May need to create a method to convert raw marks format, depends on API
# Can also change format if needed.
# raw marks format:
# Assumptions: task_weight is scaled 0 - 100 (i.e. 70 for 70% weighting)
#              subject_name should only occur once per subject
#
# {
#     subject_name : {
#         subject_task : {
#             task_weight : 70,
#              task_mark : A+
#         },
#         subject_task2 : {
#             task_weight : 30,
#             task_mark : B-
#         }
#     },
#     subject_name2...
# }

# returned format: { subject_name : converted_mark, ...}
def convert_weighted_sa(raw_marks):
    converted_marks = {}

    for subject, tasks in raw_marks.items():
        temp = 0
        for task, details in tasks.items():
            temp += convert_sa_individual(details['task_mark'].lower()) * (details['task_weight'] / 100)
        converted_marks[subject] = temp

    return converted_marks


# Converts TAS grades (EA, HA, CA, SA, PA, NN) to numerical
# Some may already be numerical (?) will have check for this
# Input data from API probably needs year as well
# Input format:
# {
#    subject_name : {
#         year : 11,
#         mark : EA
#     },
#     subject_name_1 : {
#         year: 12,
#         mark : 90
#     }
# }
# Output format: (will turn them all into numbers if they are not numbers)
# {
#     year : {
#         subjects : [ {subject: 'math', score: 90, credits: 15} ]
#     }
# }
def convert_cat_tas(raw_marks):
    converted_marks = {}
    for subject, data in raw_marks.items():
        # Extract the grade, year, and credits for the subject
        # grade = str(data.get('mark')).lower()  # Convert to lowercase to handle different case variations
        grade = data.get('mark')
        year = data.get('year')
        print(subject)
        try:
            tas_subject_instance = Tas_subject.objects.get(name=subject)
        except Tas_subject.DoesNotExist:
            # Without this, the DoesNotExist propagates uncaught, gets swallowed
            # by storage_student_score's generic except-Exception (which returns
            # None), and the user sees a confusing "'NoneType' object has no
            # attribute 'tolist'" 500 error instead of knowing which subject to fix.
            raise CustomErrorException(
                f"Subject '{subject}' is not recognised for TAS. Please check the subject name."
            )
        credits = tas_subject_instance.credits

        # Convert the grade using the mapping, or keep it unchanged if already numerical
        # converted_grade = TAS_CAT.get(grade, grade)
        # converted_grade = A_CAT.get(converted_grade, converted_grade)

        # Create a nested dictionary with subject details
        subject_details = {
            'subject': subject,
            # 'score': converted_grade,  # Assuming you want the score as an integer
            'score': grade,
            'credits': credits
        }

        # Check if the year already exists in the converted_marks dictionary
        if year not in converted_marks:
            # If the year does not exist, create a new entry with a list for subjects
            converted_marks[year] = {'subjects': []}

        # Append the subject details to the list of subjects for the current year
        converted_marks[year]['subjects'].append(subject_details)

    print('raw after convert: ', converted_marks)

    return converted_marks


# Converting IB marks to numerical, including ToKEE bonus points
# Input Format:
# {
#     subject_name: grade,
#     ...,
#     ToK: charGrade,
#     EE: charGrade
# }
# Output:
#
# {
#     subject_name: converted_grade,
#     ...,
#     ToKEE: bonus_marks
# }
def convert_ib(raw_marks):
    converted_marks = {}
    ToKEE = []

    # alphabetically ordered dictionary of
    # grade combinations tuples and corresponding points
    table_ToKEE = {
        ('A', 'A'): 3,
        ('A', 'B'): 3,
        ('A', 'C'): 2,
        ('A', 'D'): 2,
        ('A', 'E'): 1,
        ('B', 'B'): 2,
        ('B', 'C'): 1,
        ('B', 'D'): 1,
        ('B', 'E'): 0,
        ('C', 'C'): 1,
        ('C', 'D'): 0,
        ('C', 'E'): 0,
        ('D', 'D'): 0,
        ('D', 'E'): 0,
        ('E', 'E'): 0,
    }

    for subject, mark in raw_marks.items():
        print(mark)
        if subject == 'Theory of Knowledge' or subject == 'Extended Essay':
            ToKEE.append(mark.upper())
        else:
            converted_marks[subject] = int(mark)

    bonus_points = table_ToKEE.get(tuple(sorted(ToKEE)))
    converted_marks['ToKEE'] = bonus_points

    return converted_marks


# Convert ACT multi-
# raw_marks format:
# {
#     subject : {
#         type : 'major'/'minor',
#         marks:{
#           a : 1,
#           b : 1,
#           c : 0,
#           d : 1,
#           e : 2
#         }
#
#     }
# }
# output format:
# {
#     subject : {
#         type : 'major'/'minor',
#         grade: 90
#     }
# }
def convert_act(raw_marks):
    converted_marks = {}
    for subject, grades in raw_marks.items():
        temp = {}
        current_total = 0
        grade_count = 0
        temp['type'] = grades['type']
        marks = grades['marks']
        for grade, count in marks.items():
            grade_count += 1
            current_total += A_CAT[grade.lower()] * count
        temp['grade'] = current_total  ##/grade_count
        converted_marks[subject] = temp

    return converted_marks


# Section 3.3.12 in previous group 5 report
# Conversion for both numerical and categorical (assuming its ABCDE cat)
# -------------------------------------------------------------------------
# DEPENDING ON API, CODE MAY HAVE TO BE UPDATED. CURRENT IMPLEMENTATION
# ASSUMES THAT THE ALL "ABCDE" INPUTS ARE STRING, AND ALL NUMERICAL INPUTS
# ARE INTEGERS
# -------------------------------------------------------------------------
# raw_marks format:
# {
#     subject : grade (i.e. a),
#     subject2 : grade (i.e. 80)
#
# }
# ouptut format:
# {
#     subject : converted_numerical_grade (i.e. 90),
#     subject3 : 80
# }
def convert_all_qld(raw_marks):
    converted_marks = {}

    subjects = list(raw_marks.keys())
    for subject in subjects:

        print(raw_marks[subject])
        if isinstance(raw_marks[subject], int):
            converted_marks[subject] = raw_marks[subject]
            continue
        # extract the grade for the subject
        grade = raw_marks[subject][0].lower()

        # convert the grade and store in a new dictionary
        converted_marks[subject] = A_CAT.get(grade)

    return converted_marks
