import requests
import json
import pandas as pd
import random

# Replace with your actual Data Center ID and API Token
datacenter_id = 'yul1'
api_token = 'idXPUF5FTuNeGZeYJg6k5bky6BMJLXlVeWBxqcqY'

# Load the CSV file
csv_file = 'comments.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Extract comments from the CSV file
comments = df['Comment'].dropna().tolist()

# Select 10 random comments
random_comments = random.sample(comments, 10)

# Step 1: Create the Survey
survey_url = f'https://{datacenter_id}.qualtrics.com/API/v3/survey-definitions'
survey_payload = {
    'SurveyName': 'YouTube Comments Disinformation',
    'Language': 'AR',  # Adjust if necessary
    'ProjectCategory': 'CORE'
}
survey_headers = {
    'X-API-TOKEN': api_token,
    'Content-Type': 'application/json'
}

survey_response = requests.post(survey_url, headers=survey_headers, json=survey_payload)
survey_data = survey_response.json()

if survey_response.status_code == 200:
    survey_id = survey_data['result']['SurveyID']
    print(f"Survey Created: ID = {survey_id}")

    # Step 2: Add Comments as Questions to the Survey
    for idx, comment in enumerate(random_comments):
        question_url = f'https://{datacenter_id}.qualtrics.com/API/v3/survey-definitions/{survey_id}/questions'
        
        question_payload = {
            "QuestionText": f"Do you believe the following comment is disinformation?\n\n\"{comment}\"",
            "DataExportTag": f"Q{idx+1}",
            "QuestionType": "MC",
            "Selector": "SAVR",
            "SubSelector": "TX",
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "Choices": {
                "1": {
                    "Display": "Yes"
                },
                "2": {
                    "Display": "No"
                }
            },
            "ChoiceOrder": [
                "1",
                "2"
            ],
            "Validation": {
                "Settings": {
                    "ForceResponse": "ON",  # Ensure a response is required
                    "ForceResponseType": "ON",
                    "Type": "None"
                }
            },
            "Language": [],
            "NextChoiceId": 3,
            "NextAnswerId": 1,
            "QuestionID": f"QID{idx+1}",
            "QuestionText_Unsafe": f"Do you believe the following comment is disinformation?\n\n\"{comment}\""
        }
        
        question_response = requests.post(question_url, headers=survey_headers, json=question_payload)
        
        if question_response.status_code == 200:
            print(f"Question {idx+1} added successfully.")
        else:
            print(f"Failed to add Question {idx+1}: {question_response.json()}")
else:
    print(f"Failed to create survey: {survey_data}")
