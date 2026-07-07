# Params:
# units: list of mathematical units done by the student
# state: state code for the student
def find_highest_math(units, state):

    if len(units) == 0:
        return 'N/A'

    lowercase_units = [item.lower() for item in units]
    highest_unit = ''
    math_units = []

    if state == "NSW":
        # NSW's Subject table has this course as 'Mathematics Standard 1 Exam',
        # not plain 'Mathematics Standard 1' — the unqualified name never
        # matched, so it was silently unrecognised as a math subject.
        math_units = ['mathematics standard 1 exam', 'mathematics standard 2', 'mathematics advanced', 'mathematics extension 1', 'mathematics extension 2']
    elif state == "VIC":
        # 'foundation mathematics' and 'general mathematics' are lower-level
        # (pre-Unit 3/4) courses that can still appear on a transcript — added
        # below 'further mathematics' so they're recognised without outranking
        # any of the real VCE Unit 3/4 subjects.
        math_units = ['foundation mathematics', 'general mathematics', 'further mathematics', 'mathematical methods', 'specialist mathematics']
    elif state == "QLD":
        math_units = ['essential mathematics', 'general mathematics', 'mathematical methods', 'specialist mathematics']
    elif state == "TAS":
        # Lower-level/prerequisite courses (Essential Skills, Preliminary
        # stages, Mathematics 1A/1B/I/II) are ranked below 'general
        # mathematics' — this value is only ever logged to the sheet, not
        # used in any ATAR calculation, so exact relative ordering among these
        # lower tiers doesn't affect anything but which name gets displayed.
        math_units = ['essential skills - maths',
                        'essential mathematics - personal',
                        'essential mathematics - workplace',
                        'preliminary mathematics stage 1',
                        'preliminary mathematics stage 2',
                        'preliminary mathematics stage 3',
                        'preliminary mathematics stage 4',
                        'mathematics 1a',
                        'mathematics 1b',
                        'mathematics i',
                        'mathematics ii',
                        'mathematics',
                        'general mathematics',
                        # Both punctuation variants exist as separate real
                        # Subject records — a hyphen one (already matched) and
                        # an en dash (–) one that used to silently fail to match.
                        'mathematics methods - foundation',
                        'mathematics methods – foundation',
                        'mathematics methods',
                        'advanced topics in discrete mathematics',
                        'mathematics specialised',
                    ]
    elif state == "WA":
        #unsure of order
        math_units = ['mathematics applications', 'mathematics methods', 'mathematics specialist']
    elif state == "ACT":
        equivalence_map = {
                'specialist mathematics': 'mathematics advanced',
                'specialist methods': 'mathematics advanced', #not sure if we should have this one, seems there are many specialist methods for different subjects
                'mathematical methods': 'mathematics advanced',
                'mathematical applications': 'mathematics standard 2',
                'mathematics - interstate': 'mathematics standard 2',
                'mathematics - international': 'mathematics advanced',
                'further mathematics integrated': 'mathematics extension 2',
                'anu - specialist mathematics': 'mathematics extension 2',
                'anu - discrete mathematics': 'mathematics extension 2',
                'uc - discrete mathematics': 'mathematics extension 2',
        }
        new_units = []
        act_conversion = [equivalence_map.get(unit) for unit in lowercase_units]
        lowercase_units = act_conversion
        print(lowercase_units)
        math_units = ['mathematics standard 1', 'mathematics standard 2', 'mathematics advanced', 'mathematics extension 1', 'mathematics extension 2']
    elif state == "SA":
        # 99% sure this is right
        math_units = ['essential mathematics', 'general mathematics', 'mathematical methods', 'specialist mathematics']
    elif state == "IB":
        # IB Group 5 offers exactly these two courses (a student only ever
        # takes one) — Analysis & Approaches is the more rigorous/traditional
        # pure-math pathway, so it's ranked above Applications & Interpretation,
        # consistent with how the other regions order their math subjects.
        math_units = ['mathematics: applications & interpretation', 'mathematics: analysis & approaches']


    key_function = lambda unit: math_units.index(unit) if unit in math_units else float('-inf')

    highest_unit = max(lowercase_units, key=key_function, default=None)
    # ACT maps every subject through equivalence_map.get(), which returns None
    # for any non-math subject — if the student has no math subject at all,
    # highest_unit ends up None here (not a subject string), and 'math' not in
    # None used to crash with a TypeError instead of reporting no math taken.
    if highest_unit is None or 'math' not in highest_unit:
        return 'N/A'
    return highest_unit

## Testing Below

nswunits = ['english']
vicunits = ['further mathematics', 'mathematical methods', 'specialist mathematics']
qldunits = ['essential mathematics', 'general mathematics', 'mathematical methods', 'specialist mathematics']
tasunits = ['general mathematics', 'mathematics methods - foundation', 'mathematics methods', 'mathematics specialised']
waunits = ['mathematics applications', 'mathematics methods', 'mathematics specialist']
actunits = ['specialist mathematics', 'specialist methods', 'mathematical methods',
            'mathematical applications', 'mathematics - interstate', 'mathematics - international',
            'further mathematics integrated', 'anu - specialist mathematics', 'anu - discrete mathematics',
            'uc - discrete mathematics']

print(find_highest_math(nswunits, 'NSW'))
# print(find_highest_math(vicunits, 'VIC'))
# print(find_highest_math(qldunits, 'QLD'))
# print(find_highest_math(tasunits, 'TAS'))
# print(find_highest_math(waunits, 'WA'))
# print(find_highest_math(actunits, 'ACT'))


