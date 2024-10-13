import pandas as pd
from sqlalchemy import create_engine
import re  # Regular expressions for text cleaning
import html  # To escape HTML special characters
import pyodbc

# TODO: need to fix this to properly push the comments from the csv to the db.
# NOTE: these do not include the yes, no, and skip columns. Consider that implementation.
def post_comments(csv_file, batch_size=1000) -> bool:
    # Define the connection string (replace with your actual connection details)
    SERVER = 'youtube-comments.database.windows.net'
    DATABASE = 'youtube-comments'
    USERNAME = 'ameerg'
    PASSWWORD = 'I<3rizzraza'
    DRIVER = 'ODBC Driver 17 for SQL Server'

    # Create connection string for SQLAlchemy
    connection_string = f'mssql+pyodbc://{USERNAME}:{PASSWWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    
    # Load the csv file into a dataframe.
    df = pd.read_csv(csv_file, encoding='utf-8')

    # Ensure column names in DataFrame match the DB columns
    # df.columns = ['author', 'comment', 'likes', 'published_at', 'comment_id', 'yes_count', 'no_count', 'skip_count']
    
     # Batch insert into the database using pandas' to_sql method
    try:
        df.to_sql(csv_file, engine, if_exists='append', index=False, chunksize=batch_size)
        print(f"Batch insertion of {len(df)} comments successful.")
    except Exception as e:
        print(f"Error during batch insertion: {str(e)}")
        return False

    return True

if __name__ == '__main__':
    post_comments('comments-updated.csv')


