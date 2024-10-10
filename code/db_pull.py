import pandas as pd
from sqlalchemy import create_engine

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

# Print the DataFrame to see the retrieved data
print(df)
