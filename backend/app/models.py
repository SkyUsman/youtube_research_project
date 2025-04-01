# Import the db instance.
from app import db

'''
Models: define the structures of each database table.
'''

# All Comments model.
class AllComments(db.Model):
  __tablename__ = 'all_comments'
  unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  author = db.Column(db.String(255), nullable=False)
  comment = db.Column(db.Text, nullable=False)
  likes = db.Column(db.Integer, nullable=False, default=0)
  published_at = db.Column(db.DateTime, nullable=False)
  comment_id = db.Column(db.String(255), nullable=False)

# Filtered Comments model.
class FilteredComments(db.Model):
  __tablename__ = 'filtered_comments'
  unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  author = db.Column(db.String(255), nullable=False)
  comment = db.Column(db.Text, nullable=False)
  likes = db.Column(db.Integer, nullable=False, default=0)
  published_at = db.Column(db.DateTime, nullable=False)
  comment_id = db.Column(db.String(255), nullable=False)
  survey_yes = db.Column(db.Integer, nullable=True)
  survey_no = db.Column(db.Integer, nullable=True)
  survey_skip = db.Column(db.Integer, nullable=True)
