from sqlalchemy import create_engine, text

def update_db_response_counts(yes_count, no_count, skip_count):
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

    # SQL query to update the response counts
    update_query = text("""
        UPDATE yt_comments
        SET yes_count = yes_count + :yes_count,
            no_count = no_count + :no_count,
            skip_count = skip_count + :skip_count
    """)

    # Execute the update query
    with engine.connect() as connection:
        connection.execute(update_query, {'yes_count': yes_count, 'no_count': no_count, 'skip_count': skip_count})

    print("Response counts updated successfully.")
