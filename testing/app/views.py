'''
View: format the data for the responses.
Note: ** returns the data in a presentable (unpacks) format within the inital dict.
'''
# Py3 strict typing, techinally inferred.
from typing import Any

def format_comments(comments) -> list[dict[str, Any]]:
  # Guard if an error creept this far and return as is.
  if isinstance(comments, dict) and 'error' in comments:
    return comments

  # Only return the comment for now, as it is the only thing necessary to the survey (speeds it up, too).
  return [
    {
      'id': comment.unique_id,
      'comment': comment.comment
    } for comment in comments
  ]

  # Use below to add additional fields returned to the requester.
  # return [
  #   {
  #     'unique_id': comment.unique_id,
  #     'author': comment.author,
  #     'comment': comment.comment,
  #     'likes': comment.likes,
  #     'published_at': comment.published_at,
  #     'comment_id': comment.comment_id,
  #     **(
  #       {
  #         'survey_yes': comment.survey_yes,
  #         'survey_no': comment.survey_no,
  #         'survey_skip': comment.survey_skip
  #       } if hasattr(comment, 'survey_yes') else {}
  #     )
  #   } for comment in comments
  