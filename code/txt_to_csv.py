import os
import csv
from langdetect import detect, LangDetectException
from db_post import post_comments
import re  # Regular expressions for text cleaning
import html  # To escape HTML special characters

# Define the folder where your .txt files are stored
folder_path = 'comment_txt_files'  # Replace this with your folder path

# Function to check if a comment is in English
def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False  # If detection fails, assume it's not English

# Helper function to clean up the comment.
def clean_comment(comment):
    # Remove "Reply:" and any usernames or mentions
    cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()

    # Optionally remove other unnecessary characters (like punctuation, if needed)
    cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)

    # Return the cleaned comment.
    return cleaned_comment

# Format a csv file.
def txt_to_csv(csv_file):
    # Open or create a CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header for CSV file
        writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):  # Only consider .txt files
                file_path = os.path.join(folder_path, filename)
                
                # Read the content of the txt file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.read().strip().split('--------------------------------------------------')

                    # Loop through each block of comment data
                    for block in lines:
                        block = block.strip()
                        
                        if block:
                            # Parse the block to extract comment details
                            lines = block.split('\n')
                            
                            # Initialize variables for comment details
                            author, comment, likes, published_at, comment_id = "", "", 0, "", ""

                            # Extract information from each line
                            for line in lines:
                                if line.startswith("Author:"):
                                    author = line.replace("Author: ", "").strip()
                                elif line.startswith("Comment:"):
                                    comment = line.replace("Comment: ", "").strip()
                                elif line.startswith("Likes:"):
                                    likes = line.replace("Likes: ", "").strip()
                                elif line.startswith("Published At:"):
                                    published_at = line.replace("Published At: ", "").strip()
                                elif line.startswith("Comment ID:"):
                                    comment_id = line.replace("Comment ID: ", "").strip()

                            # Only include the comment if it's in English.
                            if comment and is_english(comment):
                                # Check if the number of likes is greater than 5 and the comment is long.
                                if int(likes) > 5 and 20 <= len(comment) <= 300:
                                    # Clean up the comment.
                                    comment = clean_comment(comment)
                                    
                                    # Write the parsed information to the CSV file
                                    writer.writerow([author, comment, int(likes), published_at, comment_id])

    # If we make it here, post the comments to the database.
    print("English comments successfully written to comments.csv")

    # Post the comments to the database.
    post_comments(csv_file)

if __name__ == '__main__':
    txt_to_csv('comments-updated.csv')
   