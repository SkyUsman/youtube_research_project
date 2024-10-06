import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# Define the connection string (replace with your actual connection details)
server = 'youtube-comments.database.windows.net'
database = 'youtube-comments'
username = 'username'
password = 'password'
driver = 'ODBC Driver 17 for SQL Server'

# Create connection string for SQLAlchemy
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

# Create a SQLAlchemy engine to connect to the Azure SQL database
engine = create_engine(connection_string)

# Load the CSV file into a DataFrame
csv_file_path = 'your_csv_here.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file_path)
# Drop the first column (index 0)
df = df.drop(df.columns[0], axis=1)

# Ensure column names in DataFrame match the DB columns
df.columns = ['author', 'comment', 'likes', 'published_at', 'comment_id', 'yes_count', 'no_count', 'skip_count']

# Insert the data into the SQL database table
df.to_sql('your_csv_here.csv', engine, if_exists='append', index=False)

print("Data transfer complete.")