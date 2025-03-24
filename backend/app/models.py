# Import the db instance.
from app import db

'''
Models: define the structures of each database table.
'''

# All Comments model.
class AllComments(db.Model):
  __tablename__ = 'all_comments'
  unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  author = db.Column(db.Text, nullable=False)
  comment = db.Column(db.Text, nullable=False)
  likes = db.Column(db.Integer, nullable=False)
  published_at = db.Column(db.TIMESTAMP, nullable=False)
  comment_id = db.Column(db.Text, nullable=False)

# Filtered Comments model.
class FilteredComments(db.Model):
  __tablename__ = 'filtered_comments'
  unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  author = db.Column(db.Text, nullable=False)
  comment = db.Column(db.Text, nullable=False)
  likes = db.Column(db.Integer, nullable=False)
  published_at = db.Column(db.TIMESTAMP, nullable=False)
  comment_id = db.Column(db.Text, primary_key=True, nullable=False)
  survey_yes = db.Column(db.BigInteger, nullable=True)
  survey_no = db.Column(db.BigInteger, nullable=True)
  survey_skip = db.Column(db.BigInteger, nullable=True)
