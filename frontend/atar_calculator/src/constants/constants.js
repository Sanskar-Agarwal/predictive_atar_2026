export const PROJECT_TITLE = "ATAR Calculator";
export const MIN_ROW_GENERATED = 10;

// Automatic transcript extraction requires a configured ANTHROPIC_API_KEY on
// the backend (see .env.example). Flip to true once a real key is in place.
export const AUTOMATIC_EXTRACTION_ENABLED = false;

export const DEFAULT_VALUES = { 
    'grade_type': 'Grade Type',
    'region': 'Region',
    'display_message': 'No ATAR',
};

export const REGIONS = [
    "NSW", "WA", "ACT", "VIC", "TAS", "SA", "QLD", "IB"
]

export const REGION_SUBJECT_COUNT_REQUIRED = {
    'NSW': 5,
    'WA': 5,
    'ACT': 5,
    'VIC': 4,
    'TAS': 5,
    'SA': 4,
    'QLD': 5,
    'IB': 8,
}

// Which grade types each region's backend calculator can actually consume.
// NSW/VIC/WA/QLD all normalise marks to a flat {subject: percentage} shape, so
// the generic categorical/weighted formats work for any of them. SA, TAS, ACT
// and IB each expect a distinct, incompatible shape (SACE grade points, a
// nested year structure, a type/category dict, and an IB 1-45 scale
// respectively) — pairing them with a generic grade type produces either a
// crash or a silently wrong ATAR, so they only accept their own native type.
export const REGION_GRADE_TYPES = {
    'NSW': ['Numerical', 'ABCDE', 'OHSBL', 'Numerical Weighted', 'Multiple Categorical Grade', 'Other'],
    'VIC': ['Numerical', 'ABCDE', 'OHSBL', 'Numerical Weighted', 'Multiple Categorical Grade', 'Other'],
    'WA': ['Numerical', 'ABCDE', 'OHSBL', 'Numerical Weighted', 'Multiple Categorical Grade', 'Other'],
    'QLD': ['Numerical', 'Numerical & Categorical', 'ABCDE', 'OHSBL', 'Numerical Weighted', 'Multiple Categorical Grade', 'Other'],
    'SA': ['A+ to E-', 'A+ to E- With Weighted', 'Other'],
    'TAS': ['TAS Year', 'Other'],
    'ACT': ['ACT Combined Weighted Category & Numerical', 'Other'],
    'IB': ['IB', 'Other'],
}

export const CATEGORICAL_MARK_OPTIONS = {
        'ABCDE': ['A', 'B', 'C', 'D', 'E'],
        'OHSBL': ['O', 'H', 'S', 'B', 'L'],
        'A+ to E-': [
            "A+", "A", "A-",
            "B+", "B", "B-",
            "C+", "C", "C-",
            "D+", "D", "D-",
            "E+", "E", "E-",
        ], 
        'TAS Year': [ 'EA', 'HA', 'CA', 'SA' ],
        'ACT Combined Weighted Category & Numerical' : 
    ['Major', 'Minor']
}

export const GRADE_TYPES = [
    "Numerical",
    "ABCDE",
    "OHSBL",
    "Multiple Categorical Grade",
    "Numerical Weighted",
    "A+ to E-",
    "A+ to E- With Weighted",
    "TAS Year",
    "IB",
    "ACT Combined Weighted Category & Numerical",
    "Numerical & Categorical",
    "Other"
] 

export const TABLE_HEADERS = {
    'Numerical': ['Subjects',  'Score', 'Max Score'],
    "ABCDE": [ 'Subjects', 'Score'],
    "OHSBL": [ 'Subjects', 'Score'],
    "Multiple Categorical Grade": [
        'Subjects',  
        'A','B','C','D','E'
    ],
    'Numerical Weighted': ['Subjects', 'Assessments', "Score", "Max Score", "Weighting"],
    "A+ to E-": [ 'Subject', 'Score'],
    "A+ to E- With Weighted": [ 'Subject', 'Assessment', 'Score', 'Weighting'],
    "TAS Year": ['Subject', 'Year', 'Final Rating'],
    "IB": ['Subject', 'Score'],
    "ACT Combined Weighted Category & Numerical": ['Subject', 'Type', 'A', 'B', 'C', 'D', 'E'],
    'Numerical & Categorical': ['Subject', 'Score'],
    "Other": ['Subject']
}

export const GRADE_TYPE_DESC = {
    "Numerical": "Numerical Grade Type is Doing something",
    "ABCDE":  "Numerical Grade Type is Doing something",
    "OHSBL": "Numerical Grade Type is Doing something",
    "Multiple Categorical Grade": "Numerical Grade Type is Doing something",
    "Numerical Weighted": "Numerical Grade Type is Doing something",
    "A+ to E-": "Numerical Grade Type is Doing something",
    "A+ to E- With Weighted": "Numerical Grade Type is Doing something",
    "TAS Year": "Numerical Grade Type is Doing something",
    "IB": "Numerical Grade Type is Doing something",
    "ACT Combined Weighted Category & Numerical": "Numerical Grade Type is Doing something",
    "Numerical & Categorical": "Numerical Grade Type is Doing something",
    "Other": "Numerical Grade Type is Doing something"
}

export const GRADE_TYPE_LABELS = { 
    "Numerical": "numeric",
    "ABCDE":  "categorical A,B,C,D,E",
    "OHSBL": "categorical O,H,S,B,L",
    "Multiple Categorical Grade": "categorical n=5",
    "Numerical Weighted": "numeric weighted",
    "A+ to E-": "SACE",
    "A+ to E- With Weighted": "SACE weighted",
    "TAS Year": "TAS Year",
    "IB": "IB",
    "ACT Combined Weighted Category & Numerical": "ACT",
    "Numerical & Categorical": "QLD",
    "Other": "Other"
}

export const IB_REQUIRED_SUBJECTS = [
    'Theory of Knowledge', 
    'Extended Essay'
]