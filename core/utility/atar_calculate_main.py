import pulp
import os
import shutil
import pandas as pd
from bs4 import BeautifulSoup
from scipy.interpolate import interp1d
from core.models import *
import requests

import numpy as np

import pandas as pd
import traceback

from decimal import Decimal
from bs4 import BeautifulSoup
import re

from .eligibility_check import *
import time
from scipy.stats import norm, percentileofscore


def _solve_lp(lp_problem):
    """
    Solve a PuLP problem with GLPK if it's on PATH, otherwise fall back to
    PuLP's bundled default (CBC) solver. The old code only routed to GLPK on
    'arm' CPUs and hardcoded a macOS Homebrew path — that breaks on Linux
    (e.g. Docker, where glpk-utils is installed via apt into /usr/bin) and on
    any ARM Linux host. Looking glpsol up on PATH works the same way on macOS,
    Docker, and CI regardless of architecture.
    """
    glpsol_path = shutil.which('glpsol')
    if glpsol_path:
        lp_problem.solve(pulp.GLPK_CMD(path=glpsol_path))
    else:
        lp_problem.solve()


"""
the atar_calculate_paradigm create a basic structure of all the score calculation,we use linear programming in this section
 the topnum is the top x of subjects that we want to collect, the union is the total subjects that the student learned, the maxnumofsujbect is the 
 max number of subject that can learned to the sublist, in nsw cases, 8 subject should have less than 2 categories b so the maxnumofsujbect = 2.
 excludeunion is the list of category b that the students has done in nsw cases. 
 Feel free to change it if the rules are changed ! 
"""


def nsw_atar_calculate_paradigm(units, subjects, marks, categories):
    # Create a linear programming problem
    lp_problem = pulp.LpProblem("NSW_Course_Selection", pulp.LpMaximize)

    # Create integer decision variables for each subject
    subject_vars = pulp.LpVariable.dicts("Subject", subjects, 0, 1, pulp.LpInteger)

    # Objective function: maximize the total marks
    lp_problem += pulp.lpSum([marks[i] * subject_vars[subject] for i, subject in enumerate(subjects)]), "Total_Marks"
    # print([marks[i] * subject_vars[subject] for i, subject in enumerate(subjects)])
    # print(subject_vars)
    # Constraint: select a total of 10 units
    # print([units[i] * subject_vars[subject] for i, subject in enumerate(subjects)])

    lp_problem += pulp.lpSum(
        [units[i] * subject_vars[subject] for i, subject in enumerate(subjects)]) == 10, "Select_10_Units"

    # Constraint: select at least 2 units of English courses
    lp_problem += pulp.lpSum([units[i] * subject_vars[subject] for i, subject in enumerate(subjects) if
                              'English' in subject]) >= 2, "Select_At_Least_2_English"

    # Constraint: no more than 2 units of Category B courses
    lp_problem += pulp.lpSum([units[i] * subject_vars[subject] for i, subject in enumerate(subjects) if
                              categories[i] == "Category B"]) <= 2, "Max_2_Category_B"

    # Solve the linear programming problem
    _solve_lp(lp_problem)

    # Extract the selected subjects
    selected_subjects = [subject for subject, var in subject_vars.items() if pulp.value(var) > 0.5]
    return selected_subjects


## try to use dp to solve the problem, no finish, do not use it
# def nsw_atar_calculate_paradigm(units, subjects, marks, categories, total_units=10):
#     dp = [[{"subjects": [], "total_units": 0, "total_score": 0}] * (total_units + 1) for _ in range(len(subjects) + 1)]
#
#     for i in range(1, len(subjects) + 1):
#         for j in range(1, total_units + 1):
#             current_units = units[i - 1]
#
#             # Initialize with the same data as the row above
#             dp[i][j] = dp[i - 1][j].copy()
#
#             if current_units <= j:
#                 previous_score = dp[i - 1][j - current_units]["total_score"]
#                 current_score = marks[i - 1] + previous_score
#                 try:
#                     current_subjects = dp[i - 1][j - current_units]["subjects"] + [subjects[i - 1]]
#                 except Exception as e:
#                     print(f"Error accessing subjects: {e}")
#                     print(f"i: {i}, j: {j}, current_units: {current_units}, subjects: {subjects}")
#
#                 # Check if the total units for the current selection is within the limit
#                 if dp[i][j]["total_units"] + current_units <= total_units:
#                     # Check if the current subject is English and ensure at least 2 units are selected
#                     if "English" in subjects[i - 1] and dp[i][j]["total_units"] + current_units >= 2:
#                         dp[i][j] = {"subjects": current_subjects, "total_units": dp[i][j]["total_units"] + current_units, "total_score": current_score}
#                     # Check if the current subject is in Category B and ensure at most 2 units are selected
#                     elif categories[i - 1] == "Category B" and dp[i][j]["total_units"] + current_units <= 2:
#                         dp[i][j] = {"subjects": current_subjects, "total_units": dp[i][j]["total_units"] + current_units, "total_score": current_score}
#                     # For other subjects, simply update the DP matrix
#                     elif categories[i - 1] != "Category B" and "English" not in subjects[i - 1]:
#                         dp[i][j] = {"subjects": current_subjects, "total_units": dp[i][j]["total_units"] + current_units, "total_score": current_score}
#             print(dp[i][j]["total_units"])
#
#     # Check if the final selection has exactly 10 units
#     if dp[len(subjects)][total_units]["total_units"] == total_units:
#         return dp[len(subjects)][total_units]["subjects"]
#     else:
#         print("No valid selection found with exactly 10 units.")
#         return []


def wa_calculate(converted_marks):
    ## CONVERT TO SCALED MARKS 
    # data = list(Wa_scaling.objects.all())
    subjects_list = list(converted_marks.keys())

    # wa_eligibility_check already returns a specific, human-readable reason
    # for each real WACE rule (maths co-requisite, English requirement, unit
    # count, category coverage) — but the result was only ever printed, never
    # actually enforced, so an ineligible subject combination still produced
    # a normal-looking ATAR instead of being rejected.
    is_eligible, eligibility_message = wa_eligibility_check(subjects_list)
    if not is_eligible:
        raise CustomErrorException(f"Cannot calculate a WA ATAR — {eligibility_message}")
    data = Wa_scaling.objects.all()
    wa_scaling_df = pd.DataFrame(data.values())
    if wa_scaling_df.empty:
        # handle the case when the dataframe is empty
        print('No data available for WA courses.')
        return None

    scaled_marks = {}
    wa_language_list = []
    wa_language_subjects = Subject.objects.filter(is_language=True, regionid=6)
    for subject in wa_language_subjects:
        wa_language_list.append(subject.subject)
    for subject, mark in converted_marks.items():

        '''if the subject is a language convert it to french
        all language scaling is the same but some languages
        don't have scaling data available'''
        if subject in wa_language_list:
            subject = 'French: Second Language'

        # handle the case when no matching rows are found
        # print(wa_scaling_df.columns)

        filtered_df = wa_scaling_df[wa_scaling_df['course'] == subject]
        if filtered_df.empty:
            print(subject)
            print('Subject not found in db.')
            return None

        max_scaled = wa_scaling_df['max_mark'].iloc[filtered_df.index.values[0]]
        scaled_marks[subject] = (float(mark[0] / 100) * float(max_scaled))

    ## CALCULATE THE TERTIARY ENTRANCE AGGREGATE
    agg = 0
    marks = []
    language_mark = []

    for subject, mark in scaled_marks.items():
        marks.append(mark)  # storing marks into list for sorting if Math. Methods
        if subject == 'Mathematics Methods':
            agg += 0.1 * mark  # 10 % added to aggregate
        if subject == 'Mathematics Specialist':
            agg += 0.1 * mark  # 10 % added to aggregate if Math. Specialist
        if subject in wa_language_list:
            language_mark.append(mark)  # Only 10 % of largest scaled LOTE mark considered in ATAR aggregate

    marks.sort(reverse=True)  # Sorting in descending order

    agg += sum(marks[:4])  # Top 4 scaled scores calculated
    if len(language_mark) != 0:
        agg += 0.1 * max(language_mark)  # 10 % added to aggregate if LOTE course

    ## PREDICT ATAR FROM AGGREGATE USING ONLINE CALCULATOR
    try:
        predicted_atar = wa_agg_to_atar(agg)  # oc.TISC_agg_to_ATAR(agg)
    except Exception as e:
        traceback.print_exc()
        print(f'Aggregate: {agg}')
        print(f'Scaled marks: {scaled_marks}')
        return None

    return predicted_atar


def wa_agg_to_atar(agg):
    wa_atar_list = Wa_atar.objects.all().order_by('min_tea')
    if agg < wa_atar_list.first().min_tea:
        return 30
    if agg >= wa_atar_list.last().min_tea:
        return 99.95
    num_items = wa_atar_list.count()
    for index in range(num_items - 1):
        tea_lowerbound = float(wa_atar_list[index].min_tea)
        tea_upperbound = float(wa_atar_list[index + 1].min_tea)
        atar_lowerbound = float(wa_atar_list[index].atar)
        atar_upperbound = float(wa_atar_list[index + 1].atar)
        if agg >= tea_lowerbound and agg < tea_upperbound:
            return atar_lowerbound + (agg - tea_lowerbound) / (tea_upperbound - tea_lowerbound) \
                * (atar_upperbound - atar_lowerbound)


def sa_agg_to_atar(agg):
    time1 = time.time()
    sa_atar_set = Sa_atar.objects.all().order_by('aggregate')
    sa_atar_list = []
    for e in sa_atar_set:
        sa_atar_list.append(e)
    time2 = time.time()
    print(str((time2 - time1) * 1000) + "ms")
    if agg < sa_atar_list[0].aggregate:
        return 30
    if agg >= sa_atar_list[-1].aggregate:
        return 99.95

    num_items = len(sa_atar_list)
    time3 = time.time()
    for index in range(num_items - 1):
        # print(sa_atar_list[index])
        tea_lowerbound = float(sa_atar_list[index].aggregate)
        tea_upperbound = float(sa_atar_list[index + 1].aggregate)
        # atar_lowerbound = float(sa_atar_list[index].atar)
        # atar_upperbound = float(sa_atar_list[index + 1].atar)
        if agg >= tea_lowerbound and agg < tea_upperbound:
            atar_lowerbound = float(sa_atar_list[index].atar)
            atar_upperbound = float(sa_atar_list[index + 1].atar)
            time4 = time.time()
            print(str((time4 - time3) * 1000) + "ms")
            return atar_lowerbound + (agg - tea_lowerbound) / (tea_upperbound - tea_lowerbound) \
                * (atar_upperbound - atar_lowerbound)


def sace_calculate(subject_marks):
    # check if rescaling is needed because it hasn't been received from
    # convert_sace, e.g. for NT schools
    time1 = time.time()
    needs_rescaling = False
    print(subject_marks)
    for _, mark in subject_marks.items():
        if mark[0] > 20:
            needs_rescaling = True
            break

    # rescale the marks from 0-100 to 0-20
    if needs_rescaling:
        rescaled_marks = {}
        for subject, mark in subject_marks.items():
            rescaled_mark = mark[0] / 100 * 20
            rescaled_marks[subject] = rescaled_mark
        subject_marks = rescaled_marks

    ## CALCULATE AGGREGATE

    # get a dictionary of subjects and unit counts for all SA subjects
    all_subjects = Subject.objects.filter(regionid=8)
    all_subject_units = {subject.subject: subject.units for subject in all_subjects}
    # filter it so that it only contains subjects that the student does
    subject_units = {subject: units for subject, units in all_subject_units.items() if subject in subject_marks.keys()}

    # generate a list of the subjects, in descending order by score
    subjects_ordered = sorted(subject_marks, key=subject_marks.get, reverse=True)

    # return the list of subjects with 20 units
    subjects_20 = [subject for subject, units in subject_units.items() if units == '20']

    # add the three highest 20 unit subjects to the aggregate
    aggregate = 0
    count = 0
    subjects_to_remove = []
    for subject in subjects_ordered:
        # stop once 3 subjects have been found
        if count == 3:
            break

        # check if the current subject is 20 units
        if subject in subjects_20:
            # add it to the aggregate and add 1 to count
            aggregate += subject_marks[subject]
            count += 1
            # add it to the list of subjects to remove
            subjects_to_remove.append(subject)

    # remove the 3 best 20 unit subjects from subjects_ordered
    subjects_ordered = [subject for subject in subjects_ordered if subject not in subjects_to_remove]

    # add the remaining 30 flexible units to the aggregate
    remaining_units = 30
    for subject in subjects_ordered:
        # check to see if flexible unit component is fulfilled
        if remaining_units == 0:
            break

        # get units of current subject
        units = subject_units[subject]

        if units == '20':
            # if they can use the whole subject
            if remaining_units >= 20:
                # add whole subject score to aggregate
                aggregate += subject_marks[subject]
                remaining_units -= 20
            # if they can only use half of the subject
            else:
                # add half subject score to aggregate
                aggregate += subject_marks[subject] / 2
                remaining_units -= 10

        elif units == '10':
            '''assuming that 10 unit subjects were not previously scaled to half'''
            # add half subject score to aggregate
            aggregate += subject_marks[subject] / 2
            remaining_units -= 10

    # ensure aggregate is rounded to nearest .05
    aggregate = round(aggregate * 20) / 20
    time2 = time.time()
    print("before agg to atar:" + str((time2 - time1) * 1000) + "ms")
    # print(aggregate)
    return sa_agg_to_atar(aggregate)


def tas_tes_to_atar(te_score):
    if te_score < 13:
        return 1.00
    if te_score > 130:
        return 99.95
    try:
        tas_atar_instance = Tas_atar.objects.get(tes=te_score)
        atar_value = tas_atar_instance.atar
        return atar_value
    except Tas_atar.DoesNotExist:
        # Handle the case where there is no matching te_score
        print("ATAR-TES conversion does not exist")
        return None


def update_tas_subjects():
    # Scrape tas courses page

    urls = ['https://www.tasc.tas.gov.au/students/courses/a-z/',
            'https://www.tasc.tas.gov.au/students/courses/utas/ucp/a-z/',
            'https://www.tasc.tas.gov.au/students/courses/utas/hap/a-z/']
    Tas_subject.objects.all().delete()
    for url in urls:
        # Make an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract information from the page
            subjects = soup.find_all('h5', class_='mb-1')
            credits = soup.find_all('p', class_='mb-1')

            data = list(zip([title.text.strip() for title in subjects], [credit.text.strip() for credit in credits]))
            df = pd.DataFrame(data, columns=['Subject', 'Credit'])
            df['Credit'] = df['Credit'].apply(
                lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
            print(df)

            for _, row in df.iterrows():
                # instance = Tas_subject(name=row['Subject'], credits=row['Credit'])
                # instance.save()
                instance, created = Tas_subject.objects.get_or_create(
                    name=row['Subject'],
                    credits=row['Credit']
                )

        else:
            print('Failed to retrieve the webpage. Status code:', response.status_code)


# Raw marks:
# {
#     year : {
#         subjects : [ {subject: 'math', score: 20, credits: 15} ]
#     }
# }
def tas_calculation(raw_marks):
    print('raw_marks: ', raw_marks)
    tes_total = 0
    tes_secondary = -1
    remaining_subjects = []
    primary_flag = True
    years = list(raw_marks.keys())
    print('years: ', years)
    years.sort(reverse=True)
    for year in years:
        print("year: ", year)
        print("primary: ", primary_flag)
        if primary_flag:
            tes_add, remaining_subjects = tas_calculate_main(raw_marks.get(year).get('subjects'), 45)
            tes_total += tes_add
            primary_flag = False
            if len(years) == 1:
                tes_secondary, _ = tas_calculate_main(remaining_subjects, 30)
        else:
            if tes_secondary != -1:
                temp, _ = tas_calculate_main(raw_marks.get(year).get('subjects') + remaining_subjects, 30)
                tes_secondary = max(tes_secondary, temp)
            else:
                tes_secondary, _ = tas_calculate_main(raw_marks.get(year).get('subjects') + remaining_subjects, 30)

    # Apply TES-ATAR conversion
    tes_total += tes_secondary
    print(tes_total)
    # Tas_atar maps integer TES -> ATAR, but tes_total is continuous. Round to
    # the nearest available TES and clamp to the table's range instead of an
    # exact match (which raised Tas_atar.DoesNotExist for any non-integer TES).
    tes_values = sorted(t.tes for t in Tas_atar.objects.all())
    tes_lookup = max(min(round(float(tes_total)), tes_values[-1]), tes_values[0])
    tas_instance = Tas_atar.objects.get(tes=tes_lookup)
    converted = tas_instance.atar

    print('te score: ', tes_total)
    print('converted atar: ', converted)
    return converted


def tas_apply_scaling(instance, score):
    scaling_table = {
        'SA_Min': instance.sa_min,
        'SA_Max': instance.sa_max,
        'CA_Min': instance.ca_min,
        'CA_Max': instance.ca_max,
        'HA_Min': instance.ha_min,
        'HA_Max': instance.ha_max,
        'EA_Min': instance.ea_min,
        'EA_Max': instance.ea_max,
    }

    if is_numeric(score):
        raw_score = float(score)
        grade_category = None
        for key, value in scaling_table.items():
            if 'Min' in key:
                min_key = key
                intermediate = key.replace('Min', '')
                max_key = intermediate + 'Max'
                if min_key in scaling_table and max_key in scaling_table:
                    if scaling_table[min_key] <= raw_score <= scaling_table[max_key]:
                        grade_category = key
                        break
        if grade_category:
            min_value = float(scaling_table[min_key])
            max_value = float(scaling_table[max_key])
            scaled_score = min_value + ((raw_score - min_value) / (max_value - min_value)) * (
                    float(scaling_table[grade_category]) - min_value)
            # print("subject: ", instance.course)
            print("raw score: ", score)
            print("scaled score: ", scaled_score)
            return scaled_score
        else:
            print("grade does not fall into scaling ranges")
            return raw_score
    else:
        for key, value in scaling_table.items():
            if score.upper() in key:
                min_key = key
                intermediate = key.replace('Min', '')
                max_key = intermediate + 'Max'
                break

        scaled_score = (scaling_table[min_key] + scaling_table[max_key]) / 2
        print("subject: ", instance.course)
        print("scaled score: ", scaled_score)
        return scaled_score


# Calculate part of TE score
# Apply scaling
# [ {subject: 'math', score: 19, credits: 15}, {subject: 'english', score: EA, credits: 15} ]
# Credit check (45)
def tas_calculate_main(raw_marks, credit_count):
    required_credits = credit_count
    total_score = 0
    subject_count = 0
    remaining_subjects = []
    sorted_marks = sorted(raw_marks, key=lambda x: (isinstance(x['score'], (int, float)), x['score']), reverse=True)

    for subject in sorted_marks:
        print("current subject: ", subject)
        print("required credits: ", required_credits)
        print("total_score: ", total_score)
        subject_count += 1
        course_name = subject['subject']
        score = subject['score']

        try:
            instance = Tas_scaling_alt.objects.get(course=course_name)
            score = tas_apply_scaling(instance, subject['score'])
        except:
            print("Subject is not included in scaling table")

        subj_tables = {
            'EA': 19,
            'HA': 14,
            'CA': 10,
            'SA': 7
        }

        if score in subj_tables.keys():
            score = subj_tables[score]

        required_credits -= subject['credits']
        if required_credits >= 0:
            total_score += float(score)
            if required_credits == 0:
                break
        else:
            # Total credits < 0
            used_credits = subject['credits'] + required_credits
            # fraction = float(subject['score']) * (used_credits / subject['credits'])
            fraction = float(score) * (used_credits / subject['credits'])
            subject['credits'] -= used_credits
            total_score += fraction
            remaining_subjects.append(subject)
            print("fraction: ", fraction)
            break

    for i in range(subject_count, len(raw_marks), 1):
        remaining_subjects.append(raw_marks[i])

    # BUGFIX: return the leftover subjects, not the full input list. Returning
    # raw_marks caused the secondary TES pass to re-count subjects already used
    # in the primary pass, inflating the TES (and the predicted ATAR).
    return total_score, remaining_subjects


def binary_search(arr: list, mark: float):
    '''
    Function: finds where in an ordered list any given value belongs.
    Output: neighbouring values as a list + indices of neighbouring values
    '''
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] > mark:
            left = mid + 1
        else:
            right = mid - 1
    return [arr[right], arr[left]], right, left


def linear_interp(arr: list, value, y_values: list):
    '''
    Function: linear interpolation
    Ouput: interpolation
    '''
    print("arr ", arr)
    print("y", y_values)
    print(value)
    has_nan = any(np.isnan(x) if isinstance(x, np.float64) else False for x in arr)
    nan_values = [x for x in arr if np.isnan(x)]

    print(has_nan)
    if has_nan or len(nan_values) > 0:
        X = arr[:1] + arr[-1:]
        Y = y_values[:1] + y_values[-1:]

    else:
        X, i_left, i_right = binary_search(arr, value)
        Y = [y_values[i_left], y_values[i_right]]

    interp = interp1d(X, Y)
    print("interp is ", interp(value))
    return interp(value)


def get_atar_df_by_state(state):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if state == "NSW":
        # num_rows = NSW_atar.objects.using('default').count()
        # if num_rows == 0:
        ## if the table is empty, look at the source dir
        nsw_atar_file = "atar_nsw.csv"
        absolute_path = os.path.join(base_dir, 'source', 'atar_csv', nsw_atar_file)
        df = pd.read_csv(absolute_path)
        return df

    elif state == "QLD":
        qld_atar_file = "atar_qld.csv"
        absolute_path = os.path.join(base_dir, 'source', 'atar_csv', qld_atar_file)
        df = pd.read_csv(absolute_path)
        return df

    elif state == "ACT":
        act_atar_file = "atar_act.csv"
        absolute_path = os.path.join(base_dir, 'source', 'atar_csv', act_atar_file)
        df = pd.read_csv(absolute_path)
        return df

        # else:
        #     all_records = NSW_scaling.objects.values()
        #     return pd.DataFrame.from_records(all_records)


def get_scaling_df_by_state(state):
    if state == "NSW":
        num_rows = Nsw_scaling.objects.using('default').count()
        # if num_rows == 0:
        ## if the table is empty, look at the source dir
        # if os.path.exists("../source/scaling_csv/nsw_scaling.csv"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_or_dir_name = 'nsw_scaling.csv'
        absolute_path = os.path.join(base_dir, 'source', 'scaling_csv', file_or_dir_name)
        return pd.read_csv(absolute_path)
    
    elif state == "ACT":
        pass

    elif state == "QLD":
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_or_dir_name = 'qld_scaling.csv'
        absolute_path = os.path.join(base_dir, 'source', 'scaling_csv', file_or_dir_name)
        print(absolute_path)
        return pd.read_csv(absolute_path)


## the input format should be {subject:(mark,union)}
def ib_calculation(input):
    print(input)
    subjects = list(input.keys())
    mark = [t[0] for t in list(input.values())]
    print(mark)

    score = 0
    for i in range(len(subjects)):
        score = score + mark[i]
    print("score is ", score)
    # Get the current working directory
    current_directory = os.getcwd()

    # Specify the relative path to your file or directory
    relative_path = "core/source/atar_csv/atar_ib.csv"

    # Combine the current directory with the relative path
    file_path = os.path.join(current_directory, relative_path)
    aggregation = pd.read_csv(file_path)
    agg_latest = aggregation['Score'].values.tolist()
    # Use the most recent year column automatically (de-hardcoded from '2023').
    atar_col = max([c for c in aggregation.columns if str(c).isdigit()], key=int)
    if score >= agg_latest[0]:

        predicted_atar = aggregation[atar_col].iloc[0]
    elif score <= agg_latest[-1]:
        ## the person under the lowest atar will not be considered. So we just put lowest number here
        predicted_atar = aggregation[atar_col].iloc[-1]
    else:
        try:
            predicted_atar = linear_interp(agg_latest, score, aggregation[atar_col])
        except:

            traceback.print_exc()
            raise CustomErrorException("can not get the atar file")
    print(predicted_atar)
    return predicted_atar


def qld_atar_calculate_paradigm(subjects, marks, general_subject):
    lp_problem = pulp.LpProblem("Course_Selection", pulp.LpMaximize)

    # Create integer decision variables for each subject
    subject_vars = pulp.LpVariable.dicts("Subject", subjects, 0, 1, pulp.LpInteger)

    # Objective function: maximize the total marks
    lp_problem += pulp.lpSum([marks[i] * subject_vars[subject] for i, subject in enumerate(subjects)]), "Total_Marks"
    # print([marks[i] * subject_vars[subject] for i, subject in enumerate(subjects)])
    # print(subject_vars)
    # Constraint: select a total of 10 units
    # print([units[i] * subject_vars[subject] for i, subject in enumerate(subjects)])

    lp_problem += pulp.lpSum(
        [subject_vars[subject] for subject in subjects]) == 5, "Select_5_Units"

    # Constraint: select at least 4 units of general courses
    lp_problem += pulp.lpSum([subject_vars[subject] for subject in subjects if
                              subject in general_subject]) >= 4, "Select_At_Least_4_General"

    # Solve the linear programming problem
    # (See _solve_lp: the bundled CBC solver is x86-only and crashes silently
    # on arm, which used to fall through to a fixed, wrong ATAR of 51.0.)
    _solve_lp(lp_problem)

    # Extract the selected subjects
    selected_subjects = [subject for subject, var in subject_vars.items() if pulp.value(var) > 0.5]
    return selected_subjects




## this function just simply guess the distribution of the score is uniformed,
## since we cannot find the atar aggregation table in qld
def qld_atar_distribution(x):
    # mean_score = 350
    # std_dev = 83
    # all_student_scores = np.random.normal(mean_score, std_dev, 27000)

    # Specify the range [min_value, max_value]
    min_value = 55
    max_value = 490

    # Generate 27,000 random numbers within the specified range
    all_student_scores = np.random.uniform(min_value, max_value, 27000)
    # Step 1: Rank the students
    rank = percentileofscore(all_student_scores,x)
    print("the rank is ",rank)
    if x < min_value:
        return 30
    if x > max_value:
        return 99.95
    # Step 3: Convert percentile rank to ATAR scale
    # You may adjust this conversion based on your specific requirements
    atar = 99.95 * rank * 0.01
    print("atar is ", atar)
    return atar


def qld_calculation(input):
    subjects, marks = qld_scaling(input)
    # Match General-category subjects case-insensitively. The QLD Subject table stores
    # some names with inconsistent casing (e.g. "Mathematical methods" vs the official
    # "Mathematical Methods" used on transcripts and in qld_scaling.csv). Comparing on a
    # lowercased set keeps general_subject in the input casing (so the LP's
    # "subject in general_subject" check at line ~677 still aligns) while being robust to
    # whichever capitalisation the caller supplied.
    _qld_general = {s.lower() for s in Subject.objects.filter(
        regionid_id__abbreviation='QLD', category='General').values_list('subject', flat=True)}
    general_subject = [s for s in subjects if s.lower() in _qld_general]
    course = []
    try:
        print("subject is ", subjects)
        print("marks are ", marks)
        print("general subject is ", general_subject)
        course = qld_atar_calculate_paradigm(list(subjects), marks, general_subject)
    except Exception as e:
        print(f"An calculate error occurred: {e}")
        traceback.print_exc()

    dic = dict(zip(subjects, marks))
    print(dic)
    score = 0
    for i in course:
        score += dic[i]

    # ## since qld does not have any aggreation table,
    atar_df = get_atar_df_by_state("QLD")
    agg_latest = atar_df['Aggregate'].values.tolist()

    if score > agg_latest[0]:

        predicted_atar = atar_df['ATAR'].iloc[0]
    elif score < agg_latest[-1]:
        ## the person under 50 atar will not be considered. So we just put 50 here
        predicted_atar = atar_df['ATAR'].iloc[-1]
    else:
        try:
            predicted_atar = linear_interp(agg_latest, score, atar_df['ATAR'])
        except:
            # use online calculator if scaling info is unavailable
            traceback.print_exc()
            raise CustomErrorException("can not get the atar file")
    return predicted_atar



def try_float(x):
    try:

        return float(x)
    except ValueError:
        return x


def qld_scaling(input):
    subjects = list(input.keys())
    marks = [t[0] for t in input.values()]
    scaled = []
    # print(input)
    for i in range(len(subjects)):
        # print("\033[91m {}\033[00m".format(subjects[i]))
        mark = marks[i]

        # use NSW scaling info
        scaling_df = get_scaling_df_by_state('QLD')

        scaling_df['Subject'].ffill(inplace=True)  # forward fills course names only
        scaling_df['Subject'] = scaling_df['Subject'].str.lower()

        subject_lower = subjects[i].lower()
        scale_info = scaling_df[scaling_df['Subject'] == subject_lower].reset_index()
        # scale_info = scaling_df[scaling_df['Course'].isin(subject_list)].reset_index(drop=True)

        # extracting percentile info as a list from scale_info

        mark_range = scale_info[scale_info['Result'].isin(['Raw'])].iloc[-1:, :][
            ['25%', '50%', '75%', '90%', '99%']].values.tolist()  # raw mark
        mark_range = np.array(mark_range).flatten().tolist()

        scaled_range = scale_info[scale_info['Result'].isin(['Scaled'])].iloc[-1:, :][
            ['25%', '50%', '75%', '90%', '99%']].values.tolist()  # scaled mark
        scaled_range = np.array(scaled_range).flatten().tolist()

        mark_range.reverse()
        scaled_range.reverse()
        mark_range.append(0)  # appending zeroes in case mark falls below 25th percentile
        scaled_range.append(0)

        mark_range.insert(0, 100)
        scaled_range.insert(0, 99.95)
        # if mark is above scaled range take the largest value
        if 'A' in mark_range:

            if mark == 92:
                scaled.append(float(scaled_range[mark_range.index('A')]))
            elif mark == 82:
                scaled.append(float(scaled_range[mark_range.index('B')]))
            elif mark == 72:
                scaled.append(float(scaled_range[mark_range.index('C')]))
            else:
                scaled.append(float(scaled_range[mark_range.index('C')]))
            # print("scaled mark is ", mark)
            # print(scaled)
        else:
            mark = float(mark)

            mark_range = [try_float(x) for x in mark_range]
            scaled_range = [try_float(x) for x in scaled_range]
            if mark in scale_info.iloc[0].values:
                scaled_mark = scale_info[f'{scale_info.apply(lambda row: row[row == mark].index, axis=1)[0][0]}'][1]
            elif mark > mark_range[0]:
                scaled_mark = scaled_range[0]
            else:
                reverse_mark_range = [try_float(x) for x in mark_range]
                reverse_scaled_range = [try_float(x) for x in scaled_range]
                # print(mark)
                scaled_mark = linear_interp(reverse_mark_range, mark, reverse_scaled_range)

            # print("the scaled mark is ", scaled_mark)

            try:
                scaled.append(scaled_mark.tolist())
            except AttributeError:
                scaled.append(scaled_mark)

    return subjects, scaled


## the input:
## {
# 'Dance Studies': ({'type': 'Major', 'grade': 147.2, 'category': 'T'}, 1),
# 'Drama': ({'type': 'Major', 'grade': 166.0, 'category': 'A'}, 1),
# 'Media': ({'type': 'Major', 'grade': 18.4, 'category': 'nan'}, 1),
# 'Music': ({'type': 'Major', 'grade': 73.6, 'category': 'nan'}, 1),
# 'Visual Arts': ({'type': 'Major', 'grade': 128.8, 'category': 'A'}, 1)
# }
def act_calculation_paradigm(course):
    # Sort subjects based on their grades in descending order
    sorted_subjects = dict(sorted(course.items(), key=lambda x: x[1][0]['grade'], reverse=True))

    # Printing the sorted dictionary
    # print(sorted_subjects)

    # Find the top 3 T or H major courses
    top_t_h_subjects = [subject for subject, (info_dict, _) in sorted_subjects.items() if
                        info_dict['category'] in {'T', 'H'}][
                       :3]

    # Find the other best course excluding the top 3 T or H major courses
    other_best_subject = next(
        (subject for subject, (info_dict, _) in sorted_subjects.items() if subject not in top_t_h_subjects), None)
    score = 0
    for i in top_t_h_subjects:
        score = score + course[i][0]["grade"]
    score = score + course[other_best_subject][0]["grade"] * 0.6
    return score


## the input type is
# {
#     subject : {
#         type : 'major'/'minor',
#         grade: 90
#     }
# }
def act_calculation(input):
    score = 0
    for subject, info in input.items():
        subject_instance = Subject.objects.filter(subject=subject).first()
        # print("the input is ", input)
        if subject_instance:
            # Now, you can access the 'category' attribute of the Subject instance
            category_value = subject_instance.category
            info[0]["category"] = category_value
        else:
            # Handle the case where the subject is not found
            # raise CustomErrorException("the subject: %s is not found",subject)
            info[0]["category"] = None  # or any other default value or handling you prefer

    score = act_calculation_paradigm(input)
    # print(score)
    atar_df = get_atar_df_by_state("ACT")
    # Use the most recent year column automatically (de-hardcoded from '2020').
    _act_years = [c for c in atar_df.columns if str(c).isdigit()]
    agg_latest = atar_df[max(_act_years, key=int)].values.tolist()

    if score > agg_latest[0]:

        predicted_atar = atar_df['ATAR'].iloc[0]
    elif score < agg_latest[-1]:
        ## the person under 50 atar will not be considered. So we just put 50 here
        predicted_atar = atar_df['ATAR'].iloc[-1]
    else:
        try:
            predicted_atar = linear_interp(agg_latest, score, atar_df['ATAR'])
        except:
            # use online calculator if scaling info is unavailable
            traceback.print_exc()
            raise CustomErrorException("can not get the atar file")
    return predicted_atar


# the structure of the union should be like that {subject:(mark,union)...}
def nsw_calculation(input):
    score = 0

    subjects, marks, units = nsw_scaling(input)

    categories = Subject.objects.filter(subject__in=subjects, regionid_id__abbreviation='NSW').values_list('category',
                                                                                                           flat=True)

    integer_units = [int(x) for x in units]

    # English Requirement Check — NSW/UAC requires at least 2 units of a
    # Board Developed English course (English Standard, Advanced, EAL/D,
    # Extension 1/2, Literature, etc.). Without this check, a missing English
    # subject only shows up as "Select_At_Least_2_English" being infeasible
    # inside nsw_atar_calculate_paradigm below, which is swallowed by that
    # call's try/except and silently yields an empty subject selection (score
    # 0) — mapping to the floor ATAR of 50 as if it were a genuine low score
    # rather than an eligibility failure.
    english_units = sum(u for s, u in zip(subjects, integer_units) if 'English' in s)
    if english_units < 2:
        raise CustomErrorException(
            "Must include at least 2 units of an English course (e.g. English Standard, "
            "English Advanced, English Extension 1/2, English EAL/D, Literature) for a NSW ATAR."
        )

    # NSW builds the ATAR from the best 10 units. If fewer than 10 units were
    # entered, the subject-selection solver is infeasible and the result falls
    # back to the floor (50). Flag that explicitly so a 50 from too few units is
    # not mistaken for a genuine low ATAR (e.g. missing base courses).
    NSW_REQUIRED_UNITS = 10
    total_units = sum(integer_units)
    if total_units < NSW_REQUIRED_UNITS:
        # Hard-block: too few units can't form a valid ATAR. Raise a clear message
        # (shown to the user) rather than silently defaulting to 50. Nothing is
        # logged because this propagates out before the sheet/DB write.
        raise CustomErrorException(
            f"Must provide at least {NSW_REQUIRED_UNITS} units for a NSW ATAR "
            f"(found {total_units}). Check for missing base courses."
        )

    try:
        course = nsw_atar_calculate_paradigm(integer_units, list(subjects), marks, categories)
    except Exception as e:
        print(f"An calculate error occurred: {e}")
        traceback.print_exc()

    dic = dict(zip(subjects, marks))
    # print(dic)
    for i in course:
        score += dic[i]
    # print(score)
    atar_df = get_atar_df_by_state('NSW')
    # Use the most recent year column automatically (de-hardcoded from '2022')
    # so a future cutoff refresh is a one-column drop-in.
    _year_cols = [c for c in atar_df.columns if str(c).isdigit()]
    agg_latest = atar_df[max(_year_cols, key=int)].values.tolist()

    if score > agg_latest[0]:

        predicted_atar = atar_df['ATAR'].iloc[0]
    elif score < agg_latest[-1]:
        ## the person under 50 atar will not be considered. So we just put 50 here
        predicted_atar = atar_df['ATAR'].iloc[-1]
    else:
        try:
            predicted_atar = linear_interp(agg_latest, score, atar_df['ATAR'])
        except:
            # use online calculator if scaling info is unavailable
            traceback.print_exc()
            raise CustomErrorException("can not get the atar file")

    return predicted_atar, ""


## the structure of the union should be like that {subject:(mark,unit)...} and it will return the subjects,scaled_mark and the units
def nsw_scaling(union):
    # load nsw_scaling.csv in database

    subjects = list(union.keys())

    marks = [float(t[0]) / float(t[1]) for t in union.values()]

    units = [t[1] for t in union.values()]

    if 'Mathematics Extension 1' in subjects and 'Mathematics Extension 2' in subjects:
        e1_idx = subjects.index('Mathematics Extension 1')
        e2_idx = subjects.index('Mathematics Extension 2')
        units[e1_idx] = 2
        units[e2_idx] = 2

        # remove maths adv from subject and unit lists
        if 'Mathematics Advanced' in subjects:
            idx = subjects.index('Mathematics Advanced')
            subjects.pop(idx)
            units.pop(idx)
            marks.pop(idx)
    scaled = []

    subject_list = list(subjects)
    for i in range(len(subjects)):
        mark = marks[i]
        unit = units[i]
        # use NSW scaling info
        scaling_df = get_scaling_df_by_state('NSW')

        scaling_df['Course'].ffill(inplace=True)  # forward fills course names only

        scaling_df.head(5)

        scale_info = scaling_df.groupby(scaling_df.Course).get_group(subject_list[i]).reset_index()
        # scale_info = scaling_df[scaling_df['Course'].isin(subject_list)].reset_index(drop=True)

        # extracting percentile info as a list from scale_info
        mark_range = scale_info.loc[0][-6::].tolist()  # hsc mark

        scaled_range = scale_info.loc[1][-6::].tolist()  # scaled mark

        mark_range.append(0)  # appending zeroes in case mark falls below 25th percentile
        scaled_range.append(0)

        # if mark is above scaled range take the largest value
        if mark in scale_info.iloc[0].values:
            scaled_mark = scale_info[f'{scale_info.apply(lambda row: row[row == mark].index, axis=1)[0][0]}'][1]
        elif mark > mark_range[0]:
            scaled_mark = scaled_range[0]
        else:
            reverse_mark_range = mark_range
            reverse_scaled_range = scaled_range

            scaled_mark = linear_interp(reverse_mark_range, mark, reverse_scaled_range)

        scaled.append(scaled_mark.tolist() * float(unit))

    return subjects, scaled, units


def is_numeric(value):
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False



# """the report information can be found in https://vtac.edu.au/reports for VIC region"""
# def vic_calculation(combined_dict):
#     print(combined_dict) ###### test
#     # Convert the format of combined_dict
#     modified_dict = {subject: (mark, "Uncheck") for subject, (mark, _) in combined_dict.items()}
#     print(modified_dict) ###### test

#     ## 1: Check eligibility and obtain the updated dictionary
#     checked_dict = vic_eligibility_check(modified_dict)
#     if checked_dict is None:
#         print(f"Unable to pass the eligibility check. Calculation aborted.") 
#         return False  # If not eligible, end the calculation and return False
#     print(checked_dict) ###### test

#     ## 2: Convert the original scores to scaled scores
#     scaled_dict = {}
#     for subject, (mark, contribution) in checked_dict.items():
#         scaled_score = vic_study_score_to_scaled_score(subject, mark)
#         if scaled_score is not None:  # Ensure the scaled score was successfully obtained
#             scaled_dict[subject] = (scaled_score, contribution)
#         else:
#             print(f"Unable to scale score for {subject}. Calculation aborted.")  # Print error message and abort calculation
#             return False
#     print(scaled_dict) ###### test

#     ## 3: Calculate the aggregate value
#     aggregate = vic_calculate_aggregate(scaled_dict)
#     print(aggregate) ###### test

#     ## 4: Convert the aggregate to an ATAR score
#     predicted_atar = vic_aggregate_to_atar(aggregate)
#     if predicted_atar is None:
#         print("Unable to convert aggregate to ATAR. Calculation aborted.")
#         return False  # If conversion to ATAR fails, end calculation and return False
#     print(predicted_atar) ###### test

#     return predicted_atar  # Return the predicted ATAR score


# def vic_eligibility_check(modified_dict):
#     groupings = {}
#     default_group_counter = 1  # 初始化默认分组计数器

#     for record in Vic_scaling.objects.all():
#         if record.group:
#             groupings[record.study_name] = record.group
#         else:
#             # 为没有指定group的学科分配唯一的默认分组
#             groupings[record.study_name] = f"Default{default_group_counter}"
#             default_group_counter += 1  # 更新计数器以确保每个默认分组都是唯一的
#             # print(default_group_counter) ###### test

#     # english_subjects = ["English", "English as an Additional Language", "Literature", "English Language"]
#     english_subjects = []  # 初始化空列表来存储英语研究领域的科目
#     for record in Vic_scaling.objects.all():
#         if record.group == "English Studies":
#             english_subjects.append(record.study_name)  # 将属于"English Studies"组的科目添加到列表中
#     # print(english_subjects) ###### test
            
#     english_scores = {subject: score for subject, (score, _) in modified_dict.items() if subject in english_subjects}
#     # print(english_scores) ###### test
    
#     if not english_scores:
#         return None  # 如果没有英语科目，则不符合要求

#     highest_english = max(english_scores, key=english_scores.get)
#     primary_scores = [(highest_english, english_scores[highest_english])]
#     used_groups = {groupings.get(highest_english, 'Unfound'): 1}
#     # print(used_groups) ###### test

#     # non_english_scores = sorted([(subject, score) for subject, (score, _) in modified_dict.items() if subject not in english_subjects], key=lambda x: x[1], reverse=True)
#     # 对所有科目按分数排序，包括英语科目，但排除已选的最高分英语科目
#     non_english_scores = sorted([(subject, score) for subject, (score, _) in modified_dict.items() if subject != highest_english], key=lambda x: x[1], reverse=True)
#     # print(non_english_scores) ###### test

#     for subject, score in non_english_scores:
#         if len(primary_scores) < 4:
#             group = groupings.get(subject, 'Unfound')
#             # print(groupings) ###### test
#             # print(group) ###### test
#             # print(used_groups) ###### test
#             if used_groups.get(group, 0) < 2:  # 每个组最多两个"Primary"科目
#                 primary_scores.append((subject, score))
#                 used_groups[group] = used_groups.get(group, 0) + 1
#             # print(used_groups) ###### test

#     remaining_scores = [item for item in non_english_scores if item[0] not in [score[0] for score in primary_scores]]
#     increment_scores = remaining_scores[:2]

#     for subject, _ in modified_dict.items():
#         if subject in [score[0] for score in primary_scores]:
#             modified_dict[subject] = (modified_dict[subject][0], "Primary")
#         elif subject in [score[0] for score in increment_scores]:
#             modified_dict[subject] = (modified_dict[subject][0], "Increment")
#         else:
#             modified_dict[subject] = (modified_dict[subject][0], "Unused")

#     # print(modified_dict)  ###### test
#     return modified_dict


# def vic_calculate_aggregate(scaled_dict):
#     aggregate = 0
#     # 遍历scaled_dict中的每个科目及其缩放分数和贡献类型
#     for subject, (scaled_score, contribution) in scaled_dict.items():
#         # 根据contribution的类型决定如何累加到aggregate
#         if contribution == "Primary":
#             aggregate += scaled_score  # Primary科目全分加到aggregate
#         elif contribution == "Increment":
#             aggregate += scaled_score * 0.1  # Increment科目的10%分数加到aggregate
#         # Unused科目不贡献分数到aggregate

#     # print(aggregate)  ###### test
#     return aggregate


# def vic_study_score_to_scaled_score(study_name, study_score):
#     # Query the database for scaling information based on the given study_name
#     try:
#         scaling_info = Vic_scaling.objects.get(study_name=study_name)
#     except Vic_scaling.DoesNotExist:
#         # If no scaling information is found for the given study_name, print an error message and return None
#         print(f"Scaling information for study name {study_name} not found.")
#         return None

#     # Prepare the list of known study scores and their corresponding scaled scores
#     scores = [20, 25, 30, 35, 40, 45, 50]
#     scaled_scores = [
#         float(scaling_info.scaled_score_20), float(scaling_info.scaled_score_25), float(scaling_info.scaled_score_30),
#         float(scaling_info.scaled_score_35), float(scaling_info.scaled_score_40), float(scaling_info.scaled_score_45),
#         float(scaling_info.scaled_score_50)
#     ]

#     # If the given study_score exactly matches one of the known scores, return the corresponding scaled score directly
#     if study_score in scores:
#         return scaled_scores[scores.index(study_score)]

#     # Handle cases where study_score is below the minimum known score
#     if 0 <= study_score < scores[0]:
#         return scaled_scores[0] - (scaled_scores[0] - 0) * ((scores[0] - study_score) / (scores[0] - 0))

#     # Perform linear interpolation to calculate the scaled score if the study_score falls between two known scores
#     for i in range(len(scores) - 1):
#         if scores[i] < study_score < scores[i + 1]:
#             # Calculate the interpolated score using the formula for linear interpolation
#             interpolated_score = scaled_scores[i] + (scaled_scores[i + 1] - scaled_scores[i]) * ((study_score - scores[i]) / (scores[i + 1] - scores[i]))
#             return interpolated_score

#     # If the study_score does not fall within any of the known score ranges, return None
#     return None


# def vic_aggregate_to_atar(aggregate):
#     # Attempt to find an entry where agg is between range_low and range_high
#     try:
#         # Use Django's filter method to find a matching entry
#         matching_atar_entry = Vic_atar.objects.filter(range_low__lte=aggregate, range_high__gte=aggregate).first()

#         # If a matching entry is found, return the corresponding ATAR score
#         if matching_atar_entry:
#             return matching_atar_entry.atar

#         # If no matching entry is found, return a default value, None
#         return None
#     except Exception as e:
#         # If there's an error during the query, print the error and return a default value
#         print(f"Error while querying Vic_atar: {e}")
#         return None 
