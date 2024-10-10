import pandas as pd
from sqlalchemy import create_engine
import re  # Regular expressions for text cleaning
import html  # To escape HTML special characters

def get_comments():
    # Define the connection string (replace with your actual connection details)
    server = 'youtube-comments.database.windows.net'
    database = 'youtube-comments'
    username = 'ameerg'
    password = 'I<3rizzraza'
    driver = 'ODBC Driver 17 for SQL Server'

    # Create connection string for SQLAlchemy
    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Load comments from the database
    query = "SELECT comment FROM yt_comments"
    df = pd.read_sql(query, engine)

    # Return the list of comments
    return df['comment'].dropna().tolist()

def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        # Remove "Reply:" and any usernames or mentions
        cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()

        # Optionally remove other unnecessary characters (like punctuation, if needed)
        cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)

        # Escape special HTML characters
        cleaned_comment = html.escape(cleaned_comment)

        # Add the cleaned comment to the list if it's not empty
        if cleaned_comment:
            cleaned_comments.append(cleaned_comment)
    
    return cleaned_comments
