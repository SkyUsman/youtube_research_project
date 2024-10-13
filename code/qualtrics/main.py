# main.py
import random
from db_pull import get_comments, clean_comments  # Import the cleaning function
from qualtrics import QualtricsAPI  # Import the Qualtrics API class

# Replace with your actual Data Center ID and API Token
datacenter_id = 'yul1'
api_token = 'idXPUF5FTuNeGZeYJg6k5bky6BMJLXlVeWBxqcqY'

# Initialize the Qualtrics API
qualtrics_api = QualtricsAPI(datacenter_id, api_token)

# Get comments from the database
comments = get_comments()

# Clean comments for consistency
cleaned_comments = clean_comments(comments)

# Select 10 random comments
random_comments = random.sample(cleaned_comments, 10)

# Main function to orchestrate the survey creation and activation
def main():
    survey_response = qualtrics_api.create_survey()

    if survey_response.get('meta', {}).get('httpStatus') == '200 - OK':
        survey_id = survey_response['result']['SurveyID']
        print(f"Survey Created: ID = {survey_id}")

        # Add questions to the survey
        qualtrics_api.add_questions_to_survey(survey_id, random_comments)

        # Activate the survey
        activation_response = qualtrics_api.activate_survey(survey_id)
        if activation_response.get('meta', {}).get('httpStatus') == '200 - OK':
            print("Survey activated successfully.")
        else:
            print(f"Failed to activate survey: {activation_response}")
    else:
        print(f"Failed to create survey: {survey_response}")

if __name__ == '__main__':
    main()
