from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine, text
import re
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow only this origin

# Database connection parameters
server = 'youtube-comments.database.windows.net'
database = 'youtube-comments'
username = 'ameerg'
password = 'I<3rizzraza'
driver = 'ODBC Driver 17 for SQL Server'

# Create the SQLAlchemy engine
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
engine = create_engine(connection_string)

# Function to fetch 10 random comments from the database
def get_random_comments():
    query = "SELECT TOP 10 comment FROM yt_comments ORDER BY NEWID();"
    df = pd.read_sql(query, engine)

    print("Raw comments fetched from database:")
    print(df['comment'].dropna().tolist())  # Print the raw comments

    return df['comment'].dropna().tolist()

# Function to clean the comments for HTML
def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()
        cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)
        if cleaned_comment:
            cleaned_comments.append(cleaned_comment)
    
    print("Cleaned comments:")  # Print cleaned comments
    print(cleaned_comments)
    
    return cleaned_comments

# API route to get the survey questions
@app.route('/api/getComments', methods=['GET'])
def getComments():
    comments = get_random_comments()
    cleaned_comments = clean_comments(comments)
    return jsonify(cleaned_comments)

# API route to post responses
@app.route('/api/postResponses', methods=['POST'])
def post_responses():
    data = request.get_json()  # Get the JSON data from the request
    print("Received data:", data)  # Print the received data for debugging

    # Extract counts from the request data, providing defaults if necessary
    yes_count = data.get('yes_count', 0)
    no_count = data.get('no_count', 0)
    skip_count = data.get('skip_count', 0)

    # Define the SQL query using SQLAlchemy's text() function
    update_query = text("""
        UPDATE yt_comments
        SET yes_count = yes_count + :yes_count,
            no_count = no_count + :no_count,
            skip_count = skip_count + :skip_count
    """)

    # Connect to the database and execute the query
    try:
        with engine.connect() as conn:  # Assuming 'engine' is defined globally
            conn.execute(update_query, {"yes_count": yes_count, "no_count": no_count, "skip_count": skip_count})
        
        return jsonify({"message": "Response recorded", "data": data}), 200
    except Exception as e:
        print("Error executing update query:", str(e))
        return jsonify({"message": "Error recording response", "error": str(e)}), 500

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
