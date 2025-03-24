# Import the models and db instance.
from app.models import *
from app import db

'''
Service: defining the queries (business logic).
- 200: OK (not listed below, but inferred).
- 404: not found.
- 500: interal server error.
'''

def get_all_comments():
  try:
    # Query the database.
    comments = AllComments.query.all()

    # Ensure comments are populated, else 404.
    if not comments:
      return {"error": "No comments found in AllYTComments"}, 404
    
    # If we make it this far, 200 OK (return comments).
    return comments, 200
  except Exception as e:
    return {"error": f"Database error: {str(e)}"}, 500

def get_filtered_comments():
  try:
    # Query the database.
    comments = FilteredComments.query.all()

    # Ensure comments are populated, else 404.
    if not comments:
      return {"error": "No comments found in FilteredYTComments"}, 404
    
    # If we make it this far, 200 OK (return comments).
    return comments, 200
  except Exception as e:
    return {"error": f"Database error: {str(e)}"}, 500

def get_random_filtered_comments():
  try:
    # Query the database.
    comments = FilteredComments.query.order_by(db.func.random()).limit(10).all()
    
    # Ensure comments are populated, else 404.
    if not comments:
      return {"error": "No comments found in FilteredYTComments"}, 404
    
    # If we make it this far, 200 OK (return comments).
    return comments, 200
  except Exception as e:
    return {"error": f"Database error: {str(e)}"}, 500
  
def update_survey_response(unique_id: int, response_type: str):
  try:
    # Find the comment by the id.
    comment = FilteredComments.query.filter_by(unique_id=unique_id).first()

    # Guard against invalidity.
    if not comment:
      return {"error": f"Comment with ID {unique_id} not found"}, 404
    
    # Update the relative field, if plausible.
    if response_type == 'yes':
      comment.survey_yes += 1
    elif response_type == 'no':
      comment.survey_no += 1
    elif response_type == 'skip':
      comment.survey_skip += 1
    else:
      return {"error": "Invalid response type. Use 'yes', 'no', or 'skip'."}, 400
    
    # Commit the changes to the database.
    db.session.commit()

    # Return success message.
    return {"message": f"Survey response '{response_type}' recorded for comment {unique_id}"}, 200
  
  except Exception as e:
    # Rollback to previous commit.
    db.session.rollback()
    return {"error": f"An error occurred: {str(e)}"}, 500



