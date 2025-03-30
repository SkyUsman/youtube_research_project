# Import the relative packages.
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create the flask app.
db = SQLAlchemy()

# Create the application.
def create_app():
  '''
  Initalize the flask app and db connection.
  Note: we import the models and controllers within for performance benifts and to combat circular imports (from top level) + lazy loading benifits.
  '''

  app = Flask(__name__)
  app.config.from_object(Config)
  CORS(app)

  # Init the app.
  db.init_app(app)

  # Import the models and controllers to register within SQLAlchemy.
  from app.models import AllComments, FilteredComments
  from app.controllers import blueprint
  
  # Register the controllers (blueprints).
  app.register_blueprint(blueprint)

  # Global error handler.
  @app.errorhandler(Exception)
  def handle_exception(e):
    return jsonify({"error": f"An unexpected error occurred {e}"}), 500

  # Return the app instance.
  return app
  
