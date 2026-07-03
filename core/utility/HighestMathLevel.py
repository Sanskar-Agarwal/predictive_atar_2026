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
        math_units = ['mathematics standard 1', 'mathematics standard 2', 'mathematics advanced', 'mathematics extension 1', 'mathematics extension 2']
    elif state == "VIC":
        math_units = ['further mathematics', 'mathematical methods', 'specialist mathematics']
    elif state == "QLD":
        math_units = ['essential mathematics', 'general mathematics', 'mathematical methods', 'specialist mathematics']
    elif state == "TAS":
        math_units = ['general mathematics',
                        'mathematics methods - foundation',
                        'mathematics methods',
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


    key_function = lambda unit: math_units.index(unit) if unit in math_units else float('-inf')

    highest_unit = max(lowercase_units, key=key_function, default=None)
    if 'math' not in highest_unit:
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


