# 📏 Predicative ATAR Calculator

# Google Sheets API sheet

https://docs.google.com/spreadsheets/d/1Vv1ZmO98Mkgz3bh7YDTZiLqlLWLDbx34ve7J37ZDju4/edit

## 1) Request API

🎯 Endpoint - `fill_information/selectGradeTypeAndRegion`
<!-- Requirement document : request API -->
📝 <mark>Description</mark> - 
The request API that already done: user fill the basic information and send it to the server and return the list of subject and the description of grade type The input (_example_) should be:

- region_name: New South Wale;
- grade_type : "1: Single numeric mark"; 
- application_id: alphabet string 
```json
{
    "success": {
        "subjects": [
            {
                "id": 1,
                "subject": "Aboriginal Studies",
                "units": "2",
                "category": "A",
                "regionid": 1
            },
            {
                "id": 2,
                "subject": "Ancient History",
                "units": "2",
                "category": "A",
                "regionid": 1
            }
        ],
        "grade_type": [
            {
                "id": 1,
                "description": "0-100",
                "label": "1: Single numeric mark"
            }
        ]
    }
}
```
Endpoint - 'fill_information/get_subjectinfo_from_region/'
<!-- Requirement document : request API -->
📝 <mark>Description</mark> - 
The request API that already done:  user select the region and select all the subject that should be inside the region:
- region: NSW;
```commandline
{
    "History": [
        "Ancient History",
        "Modern History",
        "History Extension"
    ],
    "Science": [
        "Biology",
        "Chemistry",
        "Earth & Environmental Science",
        "Physics",
        "Science Extension"
    ],
    "Humanities": [
        "Business Studies",
        "Economics",
        "Legal Studies",
        "Studies of Religion I",
        "Studies of Religion II"
    ],
    "Arts": [
        "Drama",
        "Music 1",
        "Music 2",
        "Music Extension",
        "Visual Arts"
    ],
    "English": [
        "English Standard",
        "English Advanced",
        "English EAL/D",
        "English Extension 1",
        "English Extension 2"
    ],
    "Maths": [
        "Mathematics Advanced",
        "Mathematics Extension 1",
        "Mathematics Extension 2"
    ],
    "Other": [
        "Aboriginal Studies",
        "Agriculture",
        "Community & Family Studies",
        "Dance",
        "Design & Technology",
        "Engineering Studies",
        "English Studies Exam",
        "Food Technology",
        "Geography",
        "Industrial Technology",
        "Information Processes & Technology",
        "Investigating Science",
        "Mathematics Standard 1 Exam",
        "Mathematics Standard 2",
        "PDH&PE",
        "Society & Culture",
        "Software Design & Development",
        "Textiles & Design",
        "Arabic Continuers",
        "Arabic Extension",
        "Armenian Continuers",
        "Chinese Beginners",
        "Chinese Continuers",
        "Chinese Extension",
        "Chinese & Literature",
        "Chinese in Context",
        "Classical Hebrew Continuers",
        "Filipino Continuers",
        "French Beginners",
        "French Continuers",
        "French Extension",
        "German Beginners",
        "German Continuers",
        "German Extension",
        "Hindi Continuers",
        "Indonesian Beginners",
        "Indonesian Continuers",
        "Indonesian Extension",
        "Italian Beginners",
        "Italian Continuers",
        "Italian Extension",
        "Japanese Beginners",
        "Japanese Continuers",
        "Japanese Extension",
        "Japanese in Context",
        "Khmer Continuers",
        "Korean Beginners",
        "Korean Continuers",
        "Korean & Literature",
        "Korean in Context",
        "Latin Continuers",
        "Latin Extension",
        "Macedonian Continuers",
        "Modern Greek Beginners",
        "Modern Greek Continuers",
        "Modern Greek Extension",
        "Modern Hebrew Continuers",
        "Persian Continuers",
        "Polish Continuers",
        "Portuguese Continuers",
        "Punjabi Continuers",
        "Russian Continuers",
        "Serbian Continuers",
        "Spanish Beginners",
        "Spanish Continuers",
        "Spanish Extension",
        "Turkish Continuers",
        "Vietnamese Continuers",
        "Automotive Exam",
        "Business Services Exam",
        "Construction Exam",
        "Electrotechnology Exam",
        "Entertainment Industry Exam",
        "Financial Services Exam",
        "Hospitality Exam",
        "Human Services Exam",
        "Information & Digital Technology\nExam",
        "Primary Industries Exam",
        "Retail Services Exam",
        "Tourism, Travel & Events Exam"
    ]
}
```
Endpoint - `/fill_information/get_atar/`
<!-- Requirement document : request API -->
📝 <mark>Description</mark> - this api use to calculate the atar of nsw region applicant and store information
the message sent to backend is :

```json
{
  "region_abbr": "NSW",
  "application_id": "000000199900",
  "subjects": {
    "ABCDE": {
      "English Extension 2": {
        "marks": "a"
      },
      "Numerical": {
        "English Extension 2":{
          "marks": "99"
        }
      }
    }
  },
  "grade_type": "ABCDE"
}
```
and the message received should be :
```commandline
{
    "atar": "94.15966386554621"
}
```
## login system 
## this is not used for now since there is no online version 
### invite by the previous user
http://localhost:8000/core/invite/
```
{
    "username":"abc",
    "password":"zxcvbnm12345",
    "invited_email":"jfc@example.com"
}
```

### login 
http://localhost:8000/core/login/
```commandline

{
    "username":"abc",
    "password":"zxcvbnm12345"
}
```
### register 
http://localhost:8000/core/register/
```commandline

{
    "email":"abc@example.com",
    "invitation_code":"24107275978258",
    "username":"abc",
    "password1":"zxcvbnm12345",
    "password2":"zxcvbnm12345"
}

```
 
# predicative_atar

the pdf extracting function should depend on java,do not forget to download java if you want to update the csv files.After you finish download java, `pip install jpype1`should be used to.

# load data into database

the data from excel or csv file can be loaded by the command like this:
```
python3 manage.py initial_database --path './Predicted_ATAR_Calculation/core/source/scaling_csv/tas_scaling.csv' --model 'Tas_scaling'

python3 manage.py initial_database --path '/Users/cccurie/Desktop/predicative_atar/core/source/scaling_csv/vic_scaling.csv' --model 'Vic_scaling'
python3 manage.py initial_database --path '/Users/cccurie/Desktop/predicative_atar/core/source/atar_csv/vic_atar.csv' --model 'Vic_atar'
```

should be used to.

## 2) Export data from db:
(not used, replaced by google sheet, see seach_application/view folder)

api : http://localhost:8000/search_applications/export_excel/


## 3) For Apple Silicon macOS
since mac changed from intel to arm, we need the install the glpk to allow the linear program lib work

```
brew install glpk

brew info glpk

```
```
lp_problem.solve(pulp.GLPK_CMD(path="/path/to/glpsol"))
```
## Frontend
for the detail of frontend. please go to see the readme file inside the frontend folder. 
