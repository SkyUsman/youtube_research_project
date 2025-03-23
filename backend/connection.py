# Flask Packages.
from flask import Flask, request, jsonify
from flask_cors import CORS

# Data Manipulation.
import pandas as pd
import numpy as np

# SQLalchemy packages.
import os
from sqlalchemy import create_engine

# Helper methods.
from DBInstance import DBInstance as db

# Init the instance and enable the cors header.
app = Flask(__name__)

# Allow all origins (for debugging)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Configuration.
class Configuration:
  DB_HOST = os.environ.get('DB_HOST', 'localhost')
  DB_PORT = os.environ.get('DB_PORT', '5432')
  DB_NAME = os.environ.get('DB_NAME', 'youtube_comments')
  DB_USER = os.environ.get('DB_USER', 'postgres')
  DB_PASS = os.environ.get('DB_PASS', 'postgres')

# Create the DB Instance.
def get_db_instance():
  return db(
    host = Configuration.DB_HOST,
    database = Configuration.DB_NAME,
    username = Configuration.DB_NAME,
    password = Configuration.DB_PASS,
    port = Configuration.DB_PORT
  )

# Helper function to convert the DataFrame to JSON response.
def df_to_response(df):
  return jsonify(df.to_dict(orient = 'records'))

# Test the db out.
@app.route('/api/test_engine', method = ['GET'])
def test_db():
  try:
    # Create DB Instance.
    db = get_db_instance()

    # Select 1.
    query = f"SELECT 1 FROM \"AllYtComments\""

    # Execute the query using DBInstance.
    df = db.get_comments(query)
    #return df_to_response(df), 200

    return jsonify({"message": "Database connection successful"}, ), 200
  except Exception as e:
    print("Database connection error:", str(e))
    return jsonify({"message": "Database connection failed", "error": str(e)}), 500

# Inital Route.
@app.route('/api', method = ['GET'])
def index():
  return "<h1>Welcome to the YouTube Comments API</h1><p>Use /api/getComments to fetch comments.</p>"

# Fetch all comments.
@app.route('/api/comments', methods=['GET'])
def get_comments():
  '''
  Get all comments or filter by parameters.
  '''

  try:
    # Init a DB Instance.
    db = get_db_instance()

    # Handle optinal query parameters.
    author = request.args.get('author')
    likes_min = request.args.get('likes_min')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    table = request.args.get('table')

    # Craft the query.
    query = f"SELECT * FROM \"{table}\""

    conditions = []
    if author:
      conditions.append(f"\"Author\" ILIKE '%{author}%'")
    if likes_min:
      conditions.append(f"\"Likes\" >= {likes_min}")
    if date_from:
      conditions.append(f"\"Published_At\" >= '{date_from}'")
    if date_to:
      conditions.append(f"\"Published_At\" <= '{date_to}'")
        
    # Add conditions to query if any exist
    if conditions:
      query += " WHERE " + " AND ".join(conditions)

    # Add order by.
    query += " ORDER BY \"Published_At\" DESC"

    # Execute the query using DBInstance.
    df = db.get_comments(query)
    return df_to_response(df), 200
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/comments/<id>', methods=['GET'])
def get_comment(id: int):
  '''
  Get a specific comment by id.
  '''

  try:
    # Init the instance.
    db = get_db_instance()

    # Extract the table.
    table = request.args.get('table')
    
    # Craft the query.
    query = f"SELECT * FROM '{table}' WHERE \"CommentID\" = '{id}'"

    # Run the query.
    df = db.get_comments(query)

    if df.empty:
      return jsonify({"error": "Comment not found"}), 404
            
    return df_to_response(df), 200
    
  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/random_comments', methods=['GET'])
def get_random_comments():
  '''
  Get 10 random comments to populate the survey.
  '''

  try:
    
    # Init a DB Instance.
    db = get_db_instance()


  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/survey_responses', methods=['POST'])
def post_survey_responses():
  try:
    pass
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  
# TODO: Ensure all the flask API's work and ensure they touch and update the db in parallel.

# TODO: ensure db connection actually works to the db.

# TODO: connect with the front-end, from there host the api and the backend and the front-end, with three sepearte containers and use yaml docker compose with docker volume to then host the volume container on aws and use that survey to present, ensuring any responses submitted on the container are sent to the db.