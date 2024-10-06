import time
import webbrowser
import requests
import json
import pandas as pd
import random

# Replace with your actual Data Center ID and API Token
datacenter_id = 'yul1'
api_token = '###############' # Use your API Token here

# Load the CSV file
csv_file = 'ahmed_ameer_combined_dataset.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Ensure the 'Yes' and 'No' columns exist
if 'Yes' not in df.columns:
    df['Yes'] = 0
if 'No' not in df.columns:
    df['No'] = 0

# Extract comments from the CSV file
comments = df['Comment'].dropna().tolist()

# Select 10 random comments
random_comments = random.sample(comments, 10)

# Step 1: Create the Survey
survey_url = f'https://{datacenter_id}.qualtrics.com/API/v3/survey-definitions'
survey_payload = {
    'SurveyName': 'YouTube Comments Disinformation',
    'Language': 'EN',  # Adjust if necessary
    'ProjectCategory': 'CORE'
}
survey_headers = {
    'X-API-TOKEN': api_token,
    'Content-Type': 'application/json'
}

# Post the survery response.
survey_response = requests.post(survey_url, headers=survey_headers, json=survey_payload)
survey_data = survey_response.json()

# If the response goes well, publish the data.
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
        
      
    # Step 3: Open the survey in the default browser
    survey_link = f'https://ousurvey.qualtrics.com/jfe/form/{survey_id}'
    print(f"Opening the survey in a browser: {survey_link}")
    webbrowser.open(survey_link)  # This will open the survey in the default browser

    # Step 4: Wait for survey responses
    print("Waiting for responses to be submitted...")

    # Step 5: Retrieve Survey Responses, assuming the above set went smooth.
    response_url = f'https://{datacenter_id}.qualtrics.com/API/v3/surveys/{survey_id}/responses'

    # Wait for the results.
    while True:
      # Fetch the results.
      responses = requests.get(response_url, headers=survey_headers, json={'format': 'json'})

      # Check if responses were retrieved successfully
      if responses.status_code == 200:
          print("Survey responses retrieved successfully.")
          
          # If so, convert to JSON.
          responses_json = responses.json()

          # Check if there are any responses.
          if "responses" in responses_json and responses_json["responses"]:
            # Loop over each response and update the counts.
            for res in responses["responses"]:
                # Grab the response's question, answer within the values.
                for qid, answer in res["values"].items():
                    # Locate the comment index, based on the the ending of the question ID.
                    comment_index = int(qid.replace("QID", '')) - 1
                    
                    # Case 1: Yes.
                    if answer == "1":
                        df.at[comment_index, 'Yes'] += 1
                    elif answer == "2":
                        df.at[comment_index, 'No'] += 1
          
            # Save the updated CSV file.
            updated_csv_file = "comments-updated.csv"
            df.to_csv(updated_csv_file, index=False)
            print(f"Updated CSV file saved as {updated_csv_file}")
            break # Exit the loop once the responses are processed.
      else:
          print(f"Failed to retrieve survey responses: {responses}")
      
      # Wait for 30 seconds before checking again
      time.sleep(30)

else:
    print(f"Failed to create survey: {survey_data}")
