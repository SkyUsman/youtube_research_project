# Import the connection between the app and the controllers.
from flask import Blueprint, Response, jsonify, request

# Import the services and views.
from app.services import *
from app.views import *

# Create the blueprint (controller).
blueprint = Blueprint('comments', __name__)

'''
Controller: define all the routes and handle each request.
'''

# GET Methods.

@blueprint.route('/comments/all', methods=['GET'])
def all_comments() -> Response:
  # Fetch the comments.
  result = get_all_comments()

  # If an error occurs, return the json of the msg and the code.
  if isinstance(result, tuple) and result[1] in (404, 500):
    return jsonify(result[0]), result[1]
  
  # Otherwise, format the comments.
  return jsonify(format_comments(result[0])), result[1]

@blueprint.route('/comments/filtered', methods=['GET'])
def filtered_comments() -> Response:
  # Fetch the comments.
  result = get_filtered_comments()

  # If an error occurs, return the json of the msg and the code.
  if isinstance(result, tuple) and result[1] in (404, 500):
    return jsonify(result[0]), result[1]
  
  # Otherwise, format the comments.
  return jsonify(format_comments(result[0])), result[1]

@blueprint.route('/comments/filtered/random', methods=['GET'])
def random_filtered_comments() -> Response:
  # Fetch the comments.
  result = get_random_filtered_comments()

  # If an error occurs, return the json of the msg and the code.
  if isinstance(result, tuple) and result[1] in (404, 500):
    return jsonify(result[0]), result[1]
  
  # Otherwise, format the comments.
  return jsonify(format_comments(result[0])), result[1]

# POST Methods.

@blueprint.route('/comments/responses', methods=['POST'])
def submit_survey_response():
  # Extact the data, id, and response.
  data = request.json

  # Extract the response array.
  responses = data.get('responses')

  # Guard against no responses.
  if not responses:
    return jsonify({"error": "No responses provided"}), 400

  # Loop over the list of data.
  for response in responses:
    # Extract the id and response type.
    unique_id = response.get('id')
    response_type = response.get('response')

    # Guard against no data.
    if not unique_id or not response_type:
      return jsonify({"error": "Missing 'id' or 'response' in request"}), 400
    
    # Update the responses for each id, res pair.
    result, status_code = update_survey_response(unique_id, response_type)

    # If there was an error during update, return it immediately
    if status_code != 200:
      return jsonify(result), status_code

  # Return a success response after all updates are complete
  return jsonify({"message": "All survey responses recorded successfully"}), 200
  