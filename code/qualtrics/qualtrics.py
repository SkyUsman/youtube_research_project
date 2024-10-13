# qualtrics.py
import requests

class QualtricsAPI:
    def __init__(self, datacenter_id, api_token):
        self.datacenter_id = datacenter_id
        self.api_token = api_token

    def create_survey(self):
        survey_url = f'https://{self.datacenter_id}.qualtrics.com/API/v3/survey-definitions'
        survey_payload = {
            'SurveyName': 'YouTube Comments Disinformation',
            'Language': 'EN',
            'ProjectCategory': 'CORE'
        }
        survey_headers = {
            'X-API-TOKEN': self.api_token,
            'Content-Type': 'application/json'
        }

        response = requests.post(survey_url, headers=survey_headers, json=survey_payload)
        return response.json()

    def add_questions_to_survey(self, survey_id, comments):
        for idx, comment in enumerate(comments):
            question_url = f'https://{self.datacenter_id}.qualtrics.com/API/v3/survey-definitions/{survey_id}/questions'

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
                    "1": {"Display": "Yes"},
                    "2": {"Display": "No"},
                    "3": {"Display" : "Skip"}
                },
                "ChoiceOrder": ["1", "2", "3"],
                "Validation": {
                    "Settings": {
                        "ForceResponse": "ON",
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

            question_response = requests.post(question_url, headers={'X-API-TOKEN': self.api_token, 'Content-Type': 'application/json'}, json=question_payload)

            if question_response.status_code == 200:
                print(f"Question {idx+1} added successfully.")
            else:
                print(f"Failed to add Question {idx+1}: {question_response.json()}")

    def activate_survey(self, survey_id):
        activate_url = f'https://{self.datacenter_id}.qualtrics.com/API/v3/survey-definitions/{survey_id}/activate'
        activate_headers = {
            'X-API-TOKEN': self.api_token,
            'Content-Type': 'application/json'
        }

        response = requests.post(activate_url, headers=activate_headers)
        return response.json()
