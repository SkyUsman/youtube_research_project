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
with open('comments-updated.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
                                # Write the parsed information to the CSV file
                                writer.writerow([author, comment, likes, published_at, comment_id])

print("English comments successfully written to comments.csv")


# BELOW IS THE CODE BEFORE THE FILTER BASED ON LIKES AND COMMENT LENGTH.

# import os
# import csv
# from langdetect import detect, LangDetectException

# # Define the folder where your .txt files are stored
# folder_path = 'comment_txt_files'  # Replace this with your folder path

# # Function to check if a comment is in English
# def is_english(text):
#     try:
#         return detect(text) == 'en'
#     except LangDetectException:
#         return False  # If detection fails, assume it's not English

# # Open or create a CSV file
# with open('comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write header for CSV file
#     writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

#     # Loop through all files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".txt"):  # Only consider .txt files
#             file_path = os.path.join(folder_path, filename)
            
#             # Read the content of the txt file with UTF-8 encoding
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 lines = file.read().strip().split('--------------------------------------------------')

#                 # Loop through each block of comment data
#                 for block in lines:
#                     block = block.strip()
#                     if block:
#                         # Parse the block to extract comment details
#                         lines = block.split('\n')
#                         if len(lines) >= 5:  # Ensure the block has all required lines
#                             author = lines[0].replace("Author: ", "").strip()
#                             comment = lines[1].replace("Comment: ", "").strip()
#                             likes = lines[2].replace("Likes: ", "").strip()
#                             published_at = lines[3].replace("Published At: ", "").strip()
#                             comment_id = lines[4].replace("Comment ID: ", "").strip()

#                             # Only include the comment if it's in English
#                             if is_english(comment):
#                                 # Write the parsed information to the CSV file
#                                 writer.writerow([author, comment, likes, published_at, comment_id])

# print("English comments successfully written to comments.csv")