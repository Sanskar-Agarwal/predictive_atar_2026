# 📚 Libraries Used

Here are a list of libraries used for creating the project (frontend only):
```
@babel/plugin-proposal-private-property-in-object@7.21.11
@testing-library/jest-dom@5.17.0
@testing-library/react@13.4.0
@testing-library/user-event@13.5.0
pdfjs-dist@4.0.379
react-app-rewired@2.2.1
react-dom@18.2.0
react-dropzone@14.2.3
react-pdf@7.7.0
react-scripts@5.0.1
react@18.2.0
web-vitals@2.1.4
```

# 📲 Capturing User Inputted Data

Each row of the table generated are given a particular **row ID**, this value is then used to stored the runtime information for each of the columns inside the particular selected row type.
The system relies on the methods of `onChange`, `onClick` to capture user input. The inputted data is then stored inside a [singleton](https://refactoring.guru/design-patterns/singleton) class named `RowDataHandler`. Using the unique row id, we identified which section of the data object to be updated/replaced. After the user pressed the submit button, the system then verifiers the input data through a chain of `RowDataVerifier` that verifies whether or not the row data matches the requirements of the backend, before sending the information to generate a predicted ATAR.<br>

Here are a list of verifiers used: 
1. `ApplicationIDVerifier`: check if the user has provided an application id
2. `RegionSelectVerifier`: check if the user has selected a region
3. `IBGradeTypeVerifer`: check if the selected grade type is **IB**, then the selected region must also **IB**
4. `SubjectCountVerifier`: check if the number of subjects meets the minimum required for each grade type.
5. `ACTGradeTypeVerifier`: check if the selected grade type is **ACT Combined Weighted Category & Numerical**, then the selected region must be **ACT**
6. `ACTRegionVerifier`: check if the selected region is **ACT**, then the selected grade type must be **ACT Combined Weighted Category & Numerical**
7. `SAGradeTypeVerifier`: check if the selected grade type is any of the **SACE ...**, then the selected region must be **SA**
8. `SARegionVerifier`: check if the selected region is **SACE**, then the selected grade type must be **SACE ...**
9. `SubjectWeightingVerifier`: check if the selected type has weighted column, verifies that all weighting must be least greater than 0%, and the sum of the weightings for a subject, must added up to at most 100%.
10. `ATARResultVerifier`: check if the backend return an ATAR value or errors. NOTE: this verifier must be placed last!

# 📏 Request Formats

🎯 **Request Type**: POST<br>
📖 **Description**: Sending required information to the backend to get the predicted ATAR<br>
📏 **Request Format**: JSONs <br>
🏛️ **Request Structure**: 

The `grade_type` tag represents the grade type that the user currently is working on. Please only retrieved the `subjects` based on the value of `grade_type`

```json
{
    "region_abbr": "NSW",
    "grade_type":  "Numerical",
    "application_id": "001", 
    "applicant_name": "Steve",
    "note": "math extension 1 & 2",
    "subjects": { 
        "Numerical": {
           "Math": {
            "mark": 90, 
            "max_mark": 100
           },
           "English": {
            "mark": 98, 
            "max_mark": 100
           }
        },
        "Numerical Weighted": {
            "Math": {
                "Math B": { 
                    "mark": 90, 
                    "max_mark": 100, 
                    "weighting": 50 
                },
                "Math A": { 
                    "mark": 90, 
                    "max_mark": 100, 
                    "weighting": 50
                }
            }, 
            "English": {
                "Poetry": { 
                    "mark": 90, 
                    "max_mark": 100, 
                    "weighting": 30 
                },
                "Literature": { 
                    "mark": 90, 
                    "max_mark": 100, 
                    "weighting": 20 
                },
                "Writing": { 
                    "mark": 90, 
                    "max_mark": 100, 
                    "weighting": 50 
                }
            }
        },
        "ABCDE": {
            "Math": {
                "mark": "A"
            },
           "English": {
                "mark": "B"
           }
        }
    }
}
```

## Different Grade Type Format


The system as of `January/2024` supports 11 grade type formats with each unique request format. The supported grade types are: 
1. Numerical 
2. ABCDE (Categorical ABCDE)
3. OHSBL (Categorical OHSBL, with O: Outstanding, H: High, S: Sound, B: Basic, L: Limited)
4. Mulitiple Categorical Grade
5. Numerical Weighted
6. SACE A+ to E- (South Australia Certificate of Education)
7. SACE A+ to E- With Weighted
8. TAS Year (Tasmania)
9. IB (International Baccalaureate)
10. ACT Combined Weighted Category & Numerical (Australian Capital Territory)
11. Numerical & Categorical (QLD: Queensland)

### Numerical

📖 **Description**: Grade type that follows the format of Subject - Mark from 0% to Max Mark% (default 100%).<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The mark and max mark column accepts values from 1 to 100%, with 1 represents 1%. 

🏛️ **Request Structure**: 
```json
{ 
    "...": "some other information", 
    "subjects": {
        "Numerical": { 
            "Subject 1": { "mark": 100, "max_mark": 100 },
            "Subject 2": { "mark": 100, "max_mark": 100 }
        }
    }
```

### ABCDE

📖 **Description**: Grade type that follows the format of Subject - Mark (A,B,C,D,E), with A being the highest mark, and E the lowest mark.<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The mark column is a drop down list with 5 available options, please select one from the option.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "ABCDE": { 
            "Subject 1": { "mark": "A"},
            "Subject 2": { "mark": "B"}
        }
    }
```

### OHSBL

📖 **Description**: Grade type that follows the format of Subject - Mark (O,H,S,B,L), with O being the highest mark, and L being the lowest mark.<br> 
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The mark column is a drop down list with 5 available options, please select one from the option.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "OHSBL": { 
            "Subject 1": { "mark": "O"},
            "Subject 2": { "mark": "H"}
        }
    }
```

### Multiple Categorical Grade

📖 **Description**: Grade type that follows the format of Subject - #Outstanding, #High, #Sound, #Basic, #Limited, with Oustanding being the highest mark, and Limited being the lowest mark.<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The rest of the columns, represents the number of time, the student has received the respective mark. For example, 3 Outstandings on 3 assessments, and 2 Sounds on 2 assessments.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "Multiple Categorical Grade": { 
            "Subject 1": { "mark": {
                "outstanding": 1,
                "high": 2,
                "sound": 1,
                "basic": 0,
                "limited": 0
            },
            "Subject 2": { "mark": {
                "outstanding": 5,
                "high": 0,
                "sound": 0,
                "basic": 0,
                "limited": 0
        }
    }
```

### Numerical Weighted

📖 **Description**: Grade type that follows the format of Subject - Assessment - Score - Max Score.<br> 
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The assessment column is a textfield that can be any value. Given there are multiple assessments for a subject, those assessments must be distinguishable from one another.<br> 
- The mark and max mark column accepts values from 1 to 100%, with 1 represents 1%.<br>
- The weighting of an assessment must be at least greater than 0%, and the total weightings of all assessments for a subject must sum up to at most 100%.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "Numerical Weighted": { 
            "Mathematics": { 
                "Quiz 1": {
                    "mark": 100, 
                    "max_mark": 100, 
                    "weighting": 20
                },
                "Final": {
                    "mark": 100, 
                    "max_mark": 100, 
                    "weighting": 80
                }
            },
            "English Advance": {
                "Quiz 1": {
                    "mark": 100, 
                    "max_mark": 100, 
                    "weighting": 20
                },
                "Quiz 2": {
                    "mark": 100, 
                    "max_mark": 100, 
                    "weighting": 30
                },
                "Final": {
                    "mark": 100, 
                    "max_mark": 100, 
                    "weighting": 50
                }
            }
        }
    }
```

### SACE A+ to E-

📖 **Description**: 
Grade type that follows the format of Subject - Grade (A+ to E-). The mark system is organised in the following format (from highest to lowest) A+, A, A-, B+, B, B-, ..., E+, E, E-.<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The mark column is a drop down list with the available options, please select one from the option.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "SACE A+ to E-": { 
            "Subject 1": { "mark": "A+"},
            "Subject 2": { "mark": "A"},
            "Subject 3": { "mark": "B"},
            "Subject 4": { "mark": "C-"},
            "Subject 5": { "mark": "A"},
            "Subject 6": { "mark": "A"}
        }
    }
```

### SACE A+ to E- With Weighted

📖 **Description**: Grade type that follows the format of Subject - Grade (A+ to E-). The mark system is organised in the following format (from highest to lowest) A+, A, A-, B+, B, B-, ..., E+, E, E-, with each subject contains different assessments of certain weightings.<br> 
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The assessment column is a textfield that can be any value. Given there are multiple assessments for a subject, those assessments must be distinguishable from one another.<br>
- The mark column is a drop down list with the available options, please select one from the option.<br>
- The weighting of an assessment must be at least greater than 0%, and the total weightings of all assessments for a subject must sum up to at most 100%.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "SACE A+ to E- With Weighted": { 
            "Mathematics": { 
                "Quiz 1": {
                    "mark": "A+", 
                    "weighting": 20
                },
                "Final": {
                    "mark": "A+", 
                    "weighting": 80
                }
            },
            "English Advance": {
                "Quiz 1": {
                    "mark": "B", 
                    "weighting": 20
                },
                "Quiz 2": {
                    "mark": "B", 
                    "weighting": 30
                },
                "Final": {
                    "mark": "C", 
                    "weighting": 50
                }
            }
        }
    }
```

### TAS Year

📖 **Description**: Grade type that follows the format of Subject - Year - Mark.<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br> 
- The year column represents the subject that the student done the subject, the minimum value for the year is the current year - 20.<br>
- The mark can be selected from one of the options of (EA, HA, CA, SA), with EA being the highest and SA being the lowest. This columns also allowed number to be entered from 1 to 100 represents 1%, 100% respectively.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "TAS Year": { 
            "Subject 1": { 
                "year": "2024",
                "mark": 22
            },
            "Subject 2": { 
                "year": "2023",
                "mark": 22
            }
        }
    }
```

### IB

📖 **Description**: Grade type that follows the format of Subject - Score.<br>
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option. There are two subjects required to be inputted, those being Theory of Knowledge and Extended Essay.<br> 
- The mark is a numerical value from 1 to 7 with 7 being the highest and 1 being the lowest. Except for Theory of Knowledge and Extended Essay, you must select from one of the value A to E, with A being the highest and E being the lowest.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "IB": { 
            "Theory of Knowledge": { "mark": "A"},
            "Extended Essay": { "mark": "A"},
            "Subject 1": { "mark": 100 },
            "Subject 2": { "mark": 100 }
        }
    }
```

### ACT Combined Weighted Category & Numerical

📖 **Description**: Grade type that follows the format of Subject, Type, #A, #B, #C, #D, #E.<br> 
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The type column represents the evaluation for assessments of a subject, there are two available options that can be selected (Major, Minor).<br> 
- The rest of the columns, represents the number of time, the student has received the respective mark. For example, 3 A on 3 assessments, and 2 B on 2 assessments.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "ACT Combined Weighted Category & Numerical": { 
            "Subject 1": { 
                "type": "Major",
                "mark": {
                    "A": 3,
                    "B": 2, 
                    "C": 0, 
                    "D": 1, 
                    "E": 0
                }
            },
            "Subject 2": { 
                "type": "Minor",
                "mark": {
                    "A": 2,
                    "B": 2, 
                    "C": 1, 
                    "D": 1, 
                    "E": 0
                }
        }
    }
```

### Numerical & Categorical 

📖 **Description**: Grade type that follows the format of Subject - Mark.<br> 
- The subject column is a textfield that can be used to look up a specific subject, but please select from one of the available option.<br>
- The mark column can be both numerical from 1 to 100%, with 1 being 1%. The user can also picked from the available options with A being the highest mark and E being the lowest mark.

🏛️ **Request Structure**:
```json
{ 
    "...": "some other information", 
    "subjects": {
        "Numerical & Categorical": { 
            "Subject 1": { "mark": "A"},
            "Subject 2": { "mark": "100"},
            "Subject 3": { "mark": "98"},
            "Subject 4": { "mark": "0"}
        }
    }
```
