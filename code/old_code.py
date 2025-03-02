
    # LLM Integration for classifying if a text is a comment.
    def llm_classifiction(self, batch_comments):
        # Configure the Generative AI Library and init the LLM.
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")

        # Prompt the LLM.
        batch_prompt = [f"Comment {i + 1}: {comment}" for i, comment in enumerate(batch_comments)]
        prompt = f"Below is a list of comments. Answer the question for each: Is the text a valid user comment with actual information claimed? Respond with 'Yes' or 'No' for each. \n" + '\n'.join(batch_prompt)
        responses = model.generate_content(prompt)
        
        # Return the output classification.
        return [response.text.strip().lower() == 'yes' for response in responses]


# Process the batch of comments.
def process_batch(batch_comments, batch_ids, writer):
    # Call the LLM on the commebnts.
    classifications = llm_classifiction(batch_comments)

    # Write the results for the validated comments to the csv files.
    for i, is_valid in enumerate(classifications):
        # If the comment is valid, write to the csv.
        if is_valid:
            # Grab the row and write to it.                
            row = batch_ids[i]
            print(row)
            writer.writerow(row)
        # Timeout for 2 seconds to avoid many API calls (free version).
        time.sleep(2)


# Format a csv file.
def txt_to_csv(csv_file, batch_size = 10):
    # Open or create a CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header for CSV file
        writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

        # Init the batch list for LLM classification.
        batch_comments, batch_ids = [], []

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
                                    # Clean up the comment from white space (subjective, may be removed).
                                    comment = clean_comment(comment)     

                                    # Append to the batch for LLM classification (done to avoid mutliple API calls and prevent weak accuracy output from LLM).
                                    batch_comments.append(comment)
                                    batch_ids.append([author, comment, int(likes), published_at, comment_id])

                                    # Process the batch when we exceed the limit.
                                    if len(batch_comments) >= batch_size:
                                        print("here:")
                                        process_batch(batch_comments, batch_ids, writer)
                                        batch_comments.clear()
                                        batch_ids.clear()

         # Process remaining comments in the last batch
        if batch_comments:
            process_batch(batch_comments, batch_ids, writer)

    # If we make it here, post the comments to the database.
    print("English comments successfully written to comments.csv")

    # Post the comments to the database.
    post_comments(csv_file)
