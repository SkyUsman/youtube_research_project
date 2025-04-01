import os
import shutil
import csv

'''
Convert the generated text files into a folder then into a csv file.
This is only done to track the unfiltered csv file.

Author: Ameer Ghazal
'''

def txt_to_folder(folder_name: str):
    '''
    Puts all the .txt files in a folder.
    '''
    # # Set the source directory (where your .txt files are located)
    source_dir = os.path.join(os.getcwd(), "code")

    # Set the destination folder within the same directory
    target_folder = os.path.join(source_dir, folder_name)

    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Move all .txt files to the target folder
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        if file.endswith(".txt") and os.path.isfile(file_path):
            try:
                shutil.move(file_path, os.path.join(target_folder, file))
                print(f"Moved: {file}")
            except Exception as e:
                print(f"Failed to move {file}: {e}")

    print("Done!")

def folder_to_csv(folder_path: str, csv_name: str):   
    # Set the source directory (where your .txt files are located)
    source_dir = os.path.join(os.getcwd(), f'code/{folder_path}')

    # Open or create a CSV file
    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header for CSV file
        writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

        # Loop through all files in the folder
        for filename in os.listdir(source_dir):
            print(filename)
            if filename.endswith(".txt"):  # Only consider .txt files
                file_path = os.path.join(source_dir, filename)
                
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

                            # Extract information from each line (uncomment below to include replies).
                            for line in lines:
                                if line.startswith("Author:"):
                                    author = line.replace("Author: ", "").strip()
                                elif line.startswith("Comment:"):
                                    comment = line.replace("Comment: ", "").strip()
                                # elif line.startswith("Reply:"):
                                #     comment = line.replace("Reply: ", "").strip()
                                elif line.startswith("Likes:"):
                                    likes = line.replace("Likes: ", "").strip()
                                elif line.startswith("Published At:"):
                                    published_at = line.replace("Published At: ", "").strip()
                                elif line.startswith("Comment ID:"):
                                    comment_id = line.replace("Comment ID: ", "").strip()

                            # Only include the comment if it's in English.
                            if comment:
                                    # Write the parsed information to the CSV file
                                    writer.writerow([author, comment, likes, published_at, comment_id])

    print(f"English comments successfully written to {csv_name}.")

if __name__ == '__main__':
    txt_to_folder('china_data_security')
    folder_to_csv('china_data_security', 'china_data_security.csv')