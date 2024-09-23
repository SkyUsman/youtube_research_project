import os
import csv
from langdetect import detect, LangDetectException

# Define the folder where your .txt files are stored
folder_path = 'comment_txt_files'  # Replace this with your folder path

# Function to check if a comment is in English
def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False  # If detection fails, assume it's not English

# Open or create a CSV file
with open('comments.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header for CSV file
    writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Only consider .txt files
            file_path = os.path.join(folder_path, filename)
            
            # Read the content of the txt file
            with open(file_path, 'r') as file:
                lines = file.read().strip().split('--------------------------------------------------')

                # Loop through each block of comment data
                for block in lines:
                    block = block.strip()
                    if block:
                        # Parse the block to extract comment details
                        lines = block.split('\n')
                        if len(lines) >= 5:  # Ensure the block has all required lines
                            author = lines[0].replace("Author: ", "").strip()
                            comment = lines[1].replace("Comment: ", "").strip()
                            likes = lines[2].replace("Likes: ", "").strip()
                            published_at = lines[3].replace("Published At: ", "").strip()
                            comment_id = lines[4].replace("Comment ID: ", "").strip()

                            # Only include the comment if it's in English
                            if is_english(comment):
                                # Write the parsed information to the CSV file
                                writer.writerow([author, comment, likes, published_at, comment_id])

print("English comments successfully written to comments.csv")
