from core.models import *

"""the report information can be found in https://vtac.edu.au/reports for VIC region"""
def vic_calculation(combined_dict):
    print(f"1--combined_dict:\n{combined_dict}") ###### test
    # Convert the format of combined_dict
    # modified_dict = {subject: (mark / 2, "Uncheck") for subject, (mark, _) in combined_dict.items()}
    modified_dict = {subject: (round(mark / 2, 2), "Uncheck") for subject, (mark, _) in combined_dict.items()}
    print(f"2--modified_dict:\n{modified_dict}") ###### test

    ## 1: Check eligibility and obtain the updated dictionary
    checked_dict = vic_eligibility_check(modified_dict)
    if checked_dict is None:
        # Previously returned False here, which (since bool is a subclass of
        # int) passed select_subjects_and_grades' isinstance(res, int) check
        # and was cast to float(False) == 0.0 — showing the user a misleading
        # "ATAR: 0.00" instead of explaining they're missing an eligible
        # English-group subject.
        raise CustomErrorException(
            "Cannot calculate a VIC ATAR — no eligible English-group subject "
            "(English, English Language, Literature, EAL, etc.) was found among the entered subjects."
        )
    print(f"3--checked_dict:\n{checked_dict}") ###### test

    ## 2: Convert the original scores to scaled scores
    scaled_dict = {}
    for subject, (mark, contribution) in checked_dict.items():
        scaled_score = vic_study_score_to_scaled_score(subject, mark)
        if scaled_score is not None:  # Ensure the scaled score was successfully obtained
            scaled_dict[subject] = (scaled_score, contribution)
        else:
            raise CustomErrorException(
                f"Cannot calculate a VIC ATAR — no scaling information was found for subject '{subject}'."
            )
    print(f"4--scaled_dict:\n{scaled_dict}") ###### test

    ## 3: Calculate the aggregate value
    aggregate = vic_calculate_aggregate(scaled_dict)
    print(f"5--aggregate: {aggregate}") ###### test

    ## 4: Convert the aggregate to an ATAR score
    predicted_atar = vic_aggregate_to_atar(aggregate)
    if predicted_atar is None:
        raise CustomErrorException(
            "Cannot calculate a VIC ATAR — the aggregate score could not be converted to an ATAR (out of supported range)."
        )
    print(f"6--predicted_atar: {predicted_atar}") ###### test

    return predicted_atar  # Return the predicted ATAR score


def vic_eligibility_check(modified_dict):
    groupings = {}
    default_group_counter = 1  # 初始化默认分组计数器

    for record in Vic_scaling.objects.all():
        if record.group:
            groupings[record.study_name] = record.group
        else:
            # 为没有指定group的学科分配唯一的默认分组
            groupings[record.study_name] = f"Default{default_group_counter}"
            default_group_counter += 1  # 更新计数器以确保每个默认分组都是唯一的
            # print(default_group_counter) ###### test

    # english_subjects = ["English", "English as an Additional Language", "Literature", "English Language"]
    english_subjects = []  # 初始化空列表来存储英语研究领域的科目
    for record in Vic_scaling.objects.all():
        if record.group == "English Studies":
            english_subjects.append(record.study_name)  # 将属于"English Studies"组的科目添加到列表中
    # print(english_subjects) ###### test
            
    english_scores = {subject: score for subject, (score, _) in modified_dict.items() if subject in english_subjects}
    # print(english_scores) ###### test
    
    if not english_scores:
        return None  # 如果没有英语科目，则不符合要求

    highest_english = max(english_scores, key=english_scores.get)
    primary_scores = [(highest_english, english_scores[highest_english])]
    used_groups = {groupings.get(highest_english, 'Unfound'): 1}
    # print(used_groups) ###### test

    # non_english_scores = sorted([(subject, score) for subject, (score, _) in modified_dict.items() if subject not in english_subjects], key=lambda x: x[1], reverse=True)
    # 对所有科目按分数排序，包括英语科目，但排除已选的最高分英语科目
    non_english_scores = sorted([(subject, score) for subject, (score, _) in modified_dict.items() if subject != highest_english], key=lambda x: x[1], reverse=True)
    # print(non_english_scores) ###### test

    for subject, score in non_english_scores:
        if len(primary_scores) < 4:
            group = groupings.get(subject, 'Unfound')
            # print(groupings) ###### test
            # print(group) ###### test
            # print(used_groups) ###### test
            if used_groups.get(group, 0) < 2:  # 每个组最多两个"Primary"科目
                primary_scores.append((subject, score))
                used_groups[group] = used_groups.get(group, 0) + 1
            print(used_groups) ###### test

    remaining_scores = [item for item in non_english_scores if item[0] not in [score[0] for score in primary_scores]]
    increment_scores = remaining_scores[:2]

    for subject, _ in modified_dict.items():
        if subject in [score[0] for score in primary_scores]:
            modified_dict[subject] = (modified_dict[subject][0], "Primary")
        elif subject in [score[0] for score in increment_scores]:
            modified_dict[subject] = (modified_dict[subject][0], "Increment")
        else:
            modified_dict[subject] = (modified_dict[subject][0], "Unused")

    # print(modified_dict)  ###### test
    return modified_dict



# def vic_eligibility_check(modified_dict):
#     groupings = {}
#     default_group_counter = 1  # Initialize default group counter

#     for record in Vic_scaling.objects.all():
#         if record.group:
#             groupings[record.study_name] = record.group
#         else:
#             # Assign a unique default group for subjects without a specified group
#             groupings[record.study_name] = f"Default{default_group_counter}"
#             default_group_counter += 1  # Update the counter to ensure each default group is unique

#     english_subjects = []  # Initialize an empty list to store subjects in the English Studies group
#     for record in Vic_scaling.objects.all():
#         if record.group == "English Studies":
#             english_subjects.append(record.study_name)  # Add subjects that are part of the "English Studies" group to the list
            
#     english_scores = {subject: score for subject, (score, _) in modified_dict.items() if subject in english_subjects}
    
#     if not english_scores:
#         return None  # Return None if there are no English subjects, indicating eligibility failure

#     highest_english = max(english_scores, key=english_scores.get)
#     primary_scores = [(highest_english, english_scores[highest_english])]
#     used_groups = {groupings.get(highest_english, 'Unfound'): 1}

#     # Sort all subjects by score, including English subjects, excluding the already selected highest-scoring English subject
#     non_english_scores = sorted([(subject, score) for subject, (score, _) in modified_dict.items() if subject != highest_english], key=lambda x: x[1], reverse=True)

#     for subject, score in non_english_scores:
#         if len(primary_scores) < 4:
#             group = groupings.get(subject, 'Unfound')
#             if used_groups.get(group, 0) < 2:  # Ensure no more than two "Primary" subjects per study area group
#                 primary_scores.append((subject, score))
#                 used_groups[group] = used_groups.get(group, 0) + 1

#     remaining_scores = [item for item in non_english_scores if item[0] not in [score[0] for score in primary_scores]]
#     increment_scores = remaining_scores[:2]

#     for subject, _ in modified_dict.items():
#         if subject in [score[0] for score in primary_scores]:
#             modified_dict[subject] = (modified_dict[subject][0], "Primary")
#         elif subject in [score[0] for score in increment_scores]:
#             modified_dict[subject] = (modified_dict[subject][0], "Increment")
#         else:
#             modified_dict[subject] = (modified_dict[subject][0], "Unused")

#     return modified_dict


def vic_calculate_aggregate(scaled_dict):
    aggregate = 0
    # Iterate through each subject in scaled_dict and its scaled score and contribution type
    for subject, (scaled_score, contribution) in scaled_dict.items():
        # Decide how to add to the aggregate based on the type of contribution
        if contribution == "Primary":
            aggregate += scaled_score  # Full score of Primary subjects is added to the aggregate
        elif contribution == "Increment":
            aggregate += scaled_score * 0.1  # 10% of the Increment subjects' scores is added to the aggregate
        # Unused subjects do not contribute to the aggregate

    return round(aggregate, 2)


def vic_study_score_to_scaled_score(study_name, study_score):
    # Query the database for scaling information based on the given study_name
    try:
        scaling_info = Vic_scaling.objects.get(study_name=study_name)
    except Vic_scaling.DoesNotExist:
        # If no scaling information is found for the given study_name, print an error message and return None
        print(f"Scaling information for study name {study_name} not found.")
        return None

    # Prepare the list of known study scores and their corresponding scaled scores
    scores = [20, 25, 30, 35, 40, 45, 50]
    scaled_scores = [
        float(scaling_info.scaled_score_20), float(scaling_info.scaled_score_25), float(scaling_info.scaled_score_30),
        float(scaling_info.scaled_score_35), float(scaling_info.scaled_score_40), float(scaling_info.scaled_score_45),
        float(scaling_info.scaled_score_50)
    ]

    # If the given study_score exactly matches one of the known scores, return the corresponding scaled score directly
    if study_score in scores:
        return scaled_scores[scores.index(study_score)]

    # Handle cases where study_score is below the minimum known score
    if 0 <= study_score < scores[0]:
        return scaled_scores[0] - (scaled_scores[0] - 0) * ((scores[0] - study_score) / (scores[0] - 0))

    # Perform linear interpolation to calculate the scaled score if the study_score falls between two known scores
    for i in range(len(scores) - 1):
        if scores[i] < study_score < scores[i + 1]:
            # Calculate the interpolated score using the formula for linear interpolation
            interpolated_score = scaled_scores[i] + (scaled_scores[i + 1] - scaled_scores[i]) * ((study_score - scores[i]) / (scores[i + 1] - scores[i]))
            return interpolated_score

    # If the study_score does not fall within any of the known score ranges, return None
    return None


def vic_aggregate_to_atar(aggregate):
    # Attempt to find an entry where agg is between range_low and range_high
    try:
        # Use Django's filter method to find a matching entry
        matching_atar_entry = Vic_atar.objects.filter(range_low__lte=aggregate, range_high__gte=aggregate).first()

        # If a matching entry is found, return the corresponding ATAR score
        if matching_atar_entry:
            return matching_atar_entry.atar

        # If no matching entry is found, return a default value, None
        return None
    except Exception as e:
        # If there's an error during the query, print the error and return a default value
        print(f"Error while querying Vic_atar: {e}")
        return None 