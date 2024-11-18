import pandas as pd
from sqlalchemy import create_engine
import re  # Regular expressions for text cleaning
import html  # To escape HTML special characters

def get_comments() -> list:
    # Define the connection string (replace with your actual connection details)
    SERVER = 'youtube-comments.database.windows.net'
    DATABASE = 'youtube-comments'
    USERNAME = 'ameerg'
    PASSWORD = 'I<3rizzraza'
    DRIVER = 'ODBC Driver 17 for SQL Server'

    # Create connection string for SQLAlchemy
    connection_string = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Load comments from the database
    query = "SELECT comment FROM yt_comments WHERE skip_count = 0;"
    df = pd.read_sql(query, engine)

    # Return the list of comments, dropping the missing ones and converting to a list.
    return df['comment'].dropna().tolist()

def clean_comments(comments) -> list:
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



