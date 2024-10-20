from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine
import re

app = Flask(__name__)

# Function to fetch 10 random comments from the database
def get_random_comments():
    server = 'youtube-comments.database.windows.net'
    database = 'youtube-comments'
    username = 'ameerg'
    password = 'I<3rizzraza'
    driver = 'ODBC Driver 17 for SQL Server'

    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
    engine = create_engine(connection_string)

    # Load 10 random comments
    query = "SELECT TOP 10 comment FROM yt_comments ORDER BY NEWID()"
    df = pd.read_sql(query, engine)

    return df['comment'].dropna().tolist()

# Function to clean the comments for HTML
def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()
        cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)
        if cleaned_comment:
            cleaned_comments.append(cleaned_comment)
    return cleaned_comments

# API route to get the survey questions
@app.route('/api/getComments', methods=['GET'])
def getComments():
    comments = get_random_comments()
    cleaned_comments = clean_comments(comments)
    return jsonify(cleaned_comments)

# # API route to get the survey questions
# @app.route('/api/postResponses', methods=['POST'])
# def postResponses():
    


# def survey_questions():
#     comments = get_random_comments()
#     cleaned_comments = clean_comments(comments)
#     return jsonify(cleaned_comments)

# Start the server
if __name__ == '__main__':
    app.run(debug=True)