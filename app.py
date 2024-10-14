import requests
import pyodbc
import random
from flask import Flask, redirect, request, jsonify

app = Flask(__name__)

# Database connection setup
server = 'youtube-comments.database.windows.net'
database = 'youtube-comments'
username = 'ahme0054'
password = 'cout<<MeepMerp>>'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Qualtrics API setup
datacenter_id = 'yul1'
api_token = 'XdIIPx6eXhArsaTS6ovv6w6ZM1W1bWZuoqzIMAGw'

@app.route('/start-survey')
def create_survey_and_redirect():
    # Step 1: Connect to the database and fetch 10 random comments
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    query = "SELECT comment_id, comment FROM dbo.yt_comments"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Select 10 random comments
    random_comments = random.sample(rows, 10)

    # Step 2: Create a new Qualtrics survey
    survey_url = f'https://{datacenter_id}.qualtrics.com/API/v3/survey-definitions'
    survey_payload = {
        'SurveyName': 'YouTube Comments Disinformation',
        'Language': 'EN',
        'ProjectCategory': 'CORE'
    }
    survey_headers = {
        'X-API-TOKEN': api_token,
        'Content-Type': 'application/json'
    }

    # Create the survey and check for errors
    survey_response = requests.post(survey_url, headers=survey_headers, json=survey_payload)
    survey_data = survey_response.json()

    # Debug: print survey creation response
    print("Survey creation response: ", survey_data)

    # Check if the 'SurveyID' is present in the response
    if 'result' in survey_data and 'SurveyID' in survey_data['result']:
        survey_id = survey_data['result']['SurveyID']
        print(f"Survey ID: {survey_id}")
    else:
        return jsonify({'error': 'Failed to create survey', 'response': survey_data}), 500

    # Step 3: Add 10 questions to the survey
    for idx, comment in enumerate(random_comments):
        question_url = f'https://{datacenter_id}.qualtrics.com/API/v3/survey-definitions/{survey_id}/questions'
        question_payload = {
            "QuestionText": f"Do you believe the following comment is disinformation?\n\n\"{comment[1]}\"",
            "DataExportTag": f"Q{idx+1}",
            "QuestionType": "MC",
            "Selector": "SAVR",
            "SubSelector": "TX",
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "Choices": {
                "1": {"Display": "Yes"},
                "2": {"Display": "No"},
                "3": {"Display": "Skip"}
            },
            "ChoiceOrder": ["1", "2", "3"],
            "Validation": {
                "Settings": {
                    "ForceResponse": "ON"
                }
            }
        }

        requests.post(question_url, headers=survey_headers, json=question_payload)

    # Step 4: Activate the survey
    activate_survey_url = f"https://{datacenter_id}.qualtrics.com/API/v3/surveys/{survey_id}/activations"
    activate_survey_payload = {
        "status": "active"
    }
    activate_response = requests.post(activate_survey_url, headers=survey_headers, json=activate_survey_payload)
    activate_data = activate_response.json()

    # Debug: Print activation response
    print("Activation response: ", activate_data)

    if activate_response.status_code != 200:
        return jsonify({'error': 'Failed to activate survey', 'response': activate_data}), 500

    # Step 5: Retrieve the anonymous survey link (use the correct /distributionLinks endpoint)
    distribution_url = f"https://{datacenter_id}.qualtrics.com/API/v3/surveys/{survey_id}/distributionLinks"
    distribution_payload = {
        "type": "Anonymous"
    }
    distribution_response = requests.post(distribution_url, headers=survey_headers, json=distribution_payload)
    distribution_data = distribution_response.json()

    # Debug: print distribution response
    print("Distribution response: ", distribution_data)

    # Safely access 'result' and 'url'
    if 'result' in distribution_data and 'url' in distribution_data['result']:
        survey_link = distribution_data['result']['url']
    else:
        # Handle the case where the response does not have the expected structure
        return jsonify({'error': 'Failed to retrieve survey link', 'response': distribution_data}), 500

    # Step 6: Redirect the user to the new survey
    return redirect(survey_link)


# New Route to handle the POST request from Qualtrics when survey is completed
@app.route('/survey-response', methods=['POST'])
def handle_survey_response():
    # Get the response data from Qualtrics
    response_data = request.json
    
    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Iterate over the responses and update the database
    for question_id, answer in response_data.items():
        # Assume answer format is a dictionary with {comment_id, yes_count, no_count, skip_count}
        comment_id = answer.get('comment_id')
        yes_count = 1 if answer['selected_choice'] == 'Yes' else 0
        no_count = 1 if answer['selected_choice'] == 'No' else 0
        skip_count = 1 if answer['selected_choice'] == 'Skip' else 0

        # Update the comment record in the database
        update_query = """
        UPDATE dbo.yt_comments
        SET yes_count = yes_count + ?, no_count = no_count + ?, skip_count = skip_count + ?
        WHERE comment_id = ?;
        """
        cursor.execute(update_query, yes_count, no_count, skip_count, comment_id)

    # Commit the changes
    conn.commit()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)
