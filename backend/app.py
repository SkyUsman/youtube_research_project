from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine, text
import re
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (for debugging)

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
    query = "SELECT TOP 10 comment_id, comment FROM yt_comments WHERE LEN(comment) >= 15 ORDER BY NEWID();"
    df = pd.read_sql(query, engine)

    print("Raw comments fetched from database:")
    print(df[['comment_id', 'comment']].dropna().to_dict(orient="records"))  # Print the raw comments with ids

    return df[['comment_id', 'comment']].dropna().to_dict(orient='records')

# Function to clean the comments for HTML
def clean_comments(comments):
    cleaned_comments = []
    for comment_data in comments:
        comment = comment_data['comment']
        cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()
        cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)
        if cleaned_comment:
            comment_data['comment'] = cleaned_comment
            cleaned_comments.append(comment_data)
    
    print("Cleaned comments:")  # Print cleaned comments
    print(cleaned_comments)
    
    return cleaned_comments

# Route to test db connection
@app.route('/api/test_db', methods=['GET'])
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        print("Database connection error:", str(e))
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500

# Route for the root URL
@app.route('/')
def index():
    return "<h1>Welcome to the YouTube Comments API</h1><p>Use /api/getComments to fetch comments.</p>"

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

    # Extract responses from the request data
    responses = data.get('responses', [])

    # Iterate through each response and update the corresponding comment in the database
    try:
        with engine.connect() as conn:
            with conn.begin():  # Start a transaction block
                for response in responses:
                    update_query = text("""
                        UPDATE yt_comments
                        SET yes_count = yes_count + :yes_count,
                            no_count = no_count + :no_count,
                            skip_count = skip_count + :skip_count
                        WHERE comment_id = :comment_id
                    """)

                    result = conn.execute(update_query, {
                        "yes_count": response.get('yes_count', 0),
                        "no_count": response.get('no_count', 0),
                        "skip_count": response.get('skip_count', 0),
                        "comment_id": response.get('comment_id')
                    })

                    if result.rowcount == 0:
                        print(f"No rows updated for comment_id: {response.get('comment_id')}")
                    else:
                        print(f"Updated {result.rowcount} rows for comment_id: {response.get('comment_id')}")

        return jsonify({"message": "Responses recorded", "data": data}), 200
    except Exception as e:
        print("Error executing update query:", str(e))
        return jsonify({"message": "Error recording responses", "error": str(e)}), 500

if __name__ == '__main__':
    app.run()

