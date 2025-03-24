# Import the relative packes.
from dotenv import load_dotenv
import os

'''
Config: establish connection to the database, using env variables for abstraction.
'''

# Load in the enviroment variables.
load_dotenv()

# Construct the configuration of DB connection.
class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False