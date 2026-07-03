from core.models import *
import pandas as pd
def wa_eligibility_check(subjects):
    """
    Check Subject Selection According to WACE Criteria
    :param subjects: list of subjects
    :return: Bool + justification if Fails
    """
    queryset = Subject.objects.filter(regionid=6)
    courses = pd.DataFrame(queryset.values())

    category_a_count = sum(courses[courses['subject'].isin(subjects)]['category'] == 'A')
    category_b_count = sum(courses[courses['subject'].isin(subjects)]['category'] == 'B')
    unit_count = sum(int(unit) for unit in courses[courses['subject'].isin(subjects)]['units'])

    ## Checking Requirements
    # Math Co-requisite Check
    if 'Mathematics Specialist' in subjects and 'Mathematics Methods' not in subjects:
        return False, 'Maths co-requisite not met'

    # English Requirement Check
    if all(eng not in subjects for eng in ['English', 'Literature', 'English as an Additional Language or Dialect']):
        return False, 'English requirements not met'

    if unit_count < 10:
        print(unit_count)
        return False, f'Not Enough Units. Need {10 - unit_count} more to qualify.'
    if any(count == 0 for count in [category_a_count, category_b_count]):
        print(category_a_count, category_b_count)
        return False, 'Not enough units from each category'
    else:
        return True, 'All eligibility checks passed'
    
