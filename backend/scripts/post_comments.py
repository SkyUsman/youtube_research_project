import csv
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Now you can import using the absolute path
from app import *
from app.models import *

'''
Post comments from a file to the relative database and table.

Author: Ameer Ghazal
'''

def upload_comments_from_csv(file_path: str, table_name: str):
  # Create app instance.
  app = create_app()

  # Post the comments relative to the context.
  with app.app_context():
    try:
      with open(file_path, mode='r', encoding='utf-8') as file:
        # Generate CSV Reader.
        csv_reader = csv.DictReader(file)

        # Determine which model.
        if table_name == "all_comments":
          model = AllComments
        elif table_name == "filtered_comments":
          model = FilteredComments
        else:
          print(f"Invalid table name: {table_name}")
          return
        
        # Insert the rows into the database.
        for row in csv_reader:
          # Generate the comment.
          comment = model(
            author = row['author'],
            comment = row['comment'],
            likes = int(row['likes']),
            published_at = row['published_at'],
            comment_id = row['comment_id']
          )

          # Add in the relevant fields, if filtered.
          if table_name == "filtered_comments":
            comment.survey_yes = int(row.get('survey_yes', 0))
            comment.survey_no = int(row.get('survey_no', 0))
            comment.survey_skip = int(row.get('survey_skip', 0))
          
          # Insert the row.
          db.session.add(comment)
        
        # Commit the changes.
        db.session.commit()
        print(f"CSV data successfully uploaded to {table_name}")

    except PermissionError as e:
      print(f"Permission denied: {str(e)}")
    except Exception as e:
      # Go back to previous session.
      db.session.rollback()
      print(f"An error occurred: {str(e)}")

def upload_all_csvs_in_folder(folder_path: str, table_name: str):
    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Guard against none.
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return

    # Process each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Processing {csv_file}...")
        upload_comments_from_csv(file_path, table_name)

if __name__ == '__main__':
  # Path to the CSV.
  folder_path = 'C:/youtube_research_project/filtered_comments'

  # Specific table to insert.
  table_name = 'filtered_comments'

  # Run the function to process the folder.
  upload_all_csvs_in_folder(folder_path, table_name)