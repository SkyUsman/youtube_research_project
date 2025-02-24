# File
import os
import csv
from typing import List, Tuple

# Functions.
from db_post import post_comments
from langdetect import detect, LangDetectException
import re

# GenAI & Async
import google.generativeai as genai
import asyncio
import aiohttp

# API Key for the Gemini LLM.
GEMENI_API_KEY = "xx"

class FilterComments:
    '''Entire pipeline, reading in comments, classifying them, and updating the database.'''
    def __init__(self, folder_path: str, api_key: str, output_csv: str, batch_size: int = 20):
        self.folder_path = folder_path
        self.output_csv = output_csv
        self.batch_size = batch_size
        self.processor = ProcessComments(folder_path)
        self.classifier = ClassifyComments(api_key)

    async def run(self):
        '''Runs the full pipeline: processing, classifying, and saving; overall, filtering.'''

        # Read in and filter the comments.
        comments = self.processor.process_comments()
        
        # Open or create a CSV file
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
        
            # Write header for CSV file
            writer.writerow(['Author', 'Comment', 'Likes', 'Published At', 'Comment ID'])

            # Process comments in batches.
            batch_comments, batch_ids = [], []

            print('here')

            for data in comments:
                # Extract the data and append relatively to the batch.
                author, comment, likes, published_at, comment_id = data
                batch_comments.append(comment)
                batch_ids.append([author, comment, likes, published_at, comment_id])

                # Check if the batch limit has been exceeded; process; clear.
                if len(batch_comments) >= self.batch_size:
                    await self._process_batch(batch_comments, batch_ids, writer)
                    batch_comments.clear()
                    batch_ids.clear()
            
            # Process remaining comments if in the last batch.
            if batch_comments:
                await self._process_batch(batch_comments, batch_ids, writer)
            
        # Print for sucess and update the database.
        print(f"Comments successfully written to {self.output_csv}")

        # TODO: Update the database.
        post_comments(self.output_csv)

    async def _process_batch(self, batch_comments: List[str], batch_ids, writer):
        '''Process a batch of comments and write the valid ones to the CSV.'''
        
        # Call the LLM on the commebnts.
        classifications = await self.classifier.classify_comments(batch_comments)
        print(len(classifications))

        # Write the results for the validated comments to the csv files.
        for i, is_valid in enumerate(classifications):
            # If the comment is valid, write to the csv.
            if is_valid:
                # Grab the row and write to it.                
                row = batch_ids[i]
                writer.writerow(row)

class ClassifyComments:
    '''
    Handle the LLM-classification of the comments.
    '''
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.session = None
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={api_key}"

        self.inital_prompt = """You are a content classifier. Your task is to determine whether a comment contains meaningful information or makes a claim that could be controversial. 

        A meaningful comment must have a clear opinion, claim, or verifiable statement. Respond with 'Yes' if the comment is meaningful and 'No' otherwise.

        **Examples:**
        **Good comment (Valid)**: 
        "I believe this video provides misleading information about nutrition because multiple studies suggest otherwise." → **Yes**
        
        **Bad comment (Invalid)**: 
        "Lol this is so funny!" → **No**

        ***Good comment (Valid)**:
        "The 2009's in America was great for the American economy" -> **Yes**, as it provides a claim to something that any person could decipher as misinformation or not (in this case, misinformation, since this is when the recession happened).
        
        **Bad comment (Invalid)**: 
        "Nice vid" → **No**, since there is no value provided or claim made. It is subjective.
        
        Now, classify the following comments:
        """

    def _init_llm(self):
        '''Configure the LLM of choice.'''
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

    async def classify_comments(self, batch_comments: List[str]) -> List[bool] | None:
        '''Uses the model to classify a batch of comments.'''

        # Generate the client.
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            print('here 2')
            # Append batch comments
            batch_prompt = [f"Comment {i + 1}: {comment}" for i, comment in enumerate(batch_comments)]
            full_prompt = self.inital_prompt + '\n'.join(batch_prompt)

            # Prepare the payload.
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }]
            }

            # Make the API call to the Gemini LLM (doing this to avoid too many calls).
            async with self.session.post(
                self.base_url,
                headers={"Content-Type": "application/json"},
                json=payload
            ) as response:
                if response.status == 200:
                    # Await the data.
                    data = await response.json()

                    # Extract the text response.
                    response_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

                    # Grab the results
                    results = response_text.strip().split("\n")
                    return [result.strip().lower() == 'yes' for result in results]
                else:
                    print(f"API request failed: {response.status}")
                    print(f"{response.text}")
        except Exception as e:
            print(f"Error in LLM classification: {e}")
    
    async def close(self):
        '''Close up the session.'''
        if self.session:
            await self.session.close()

class ProcessComments:
    '''
    Read, clean, and filter youtube comments from the generated text files with llm classification.
    '''
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
    
    def _is_english(self, comment: str) -> bool:
        '''Check if a comment is in english. '''
        try:
            return detect(comment) == 'en'
        except LangDetectException:
            return False  # If detection fails, assume it's not English

    def _clean_comment(self, comment: str) -> str:
        '''Remove unwanted prefix and suffix text, cleaning up comments.'''
        # Remove "Reply:" and any usernames or mentions
        cleaned_comment = re.sub(r'Reply:\s*|\@\w+', '', comment).strip()

        # Optionally remove other unnecessary characters (like punctuation, if needed)
        cleaned_comment = re.sub(r'[^\w\s.,!?]', '', cleaned_comment)

        # Return the cleaned comment.
        return cleaned_comment

    def _parse_comment_block(self, block: str) -> Tuple[str, str, int, str, str]:
        '''Extract the comment details from a valid comment block (text).'''

         # Parse the block to extract comment details
        lines = block.split('\n')

        # Store the inital values.
        author, comment, likes, published_at, comment_id = "", "", 0, "", ""
                            
        # Extract information from each line
        for line in lines:
            if line.startswith("Author:"):
                author = line.replace("Author: ", "").strip()
            elif line.startswith("Comment:"):
                comment = line.replace("Comment: ", "").strip()
            elif line.startswith("Likes:"):
                likes = int(line.replace("Likes: ", "").strip())
            elif line.startswith("Published At:"):
                published_at = line.replace("Published At: ", "").strip()
            elif line.startswith("Comment ID:"):
                comment_id = line.replace("Comment ID: ", "").strip()

        # Return the details.
        return (author, comment, likes, published_at, comment_id)

    def process_comments(self) -> List[Tuple[str, str, int, str, str]]:
        '''Reads the comments from the files an processes them into batches to be classified.'''
        
        # Store the comments to be returned.
        filtered_comments = []

        # Loop through all files in the folder
        for filename in os.listdir(self.folder_path):
             # Only consider .txt files
            if filename.endswith(".txt"):
                # Extract the filepath.
                file_path = os.path.join(self.folder_path, filename)
                
                # Read the content of the txt file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    blocks = file.read().strip().split('--------------------------------------------------')

                    # Loop through each block of comment data
                    for block in blocks:
                        # Strip the leading and trailing whitespace.
                        block = block.strip()
                        
                        # Extract the comment details from the block, if it is a valid block.
                        if block:                            
                            # Extract the data from the tuple.
                            author, comment, likes, published_at, comment_id = self._parse_comment_block(block)

                            # If the comment has details, filter.
                            if (comment and self._is_english(comment)
                                and likes > 5 and 20 <= len(comment) <= 300):

                                # Clean up the comment.
                                cleaned_comment = self._clean_comment(comment)

                                # Append to the filtered comments.
                                filtered_comments.append((author, cleaned_comment, likes, published_at, comment_id))

        return filtered_comments

async def main():
    # Define the folder where your .txt files are stored
    folder_path = '../comment_txt_files'

    # API Key for the Gemini LLM (change to yours).
    api_key = GEMENI_API_KEY

    # Define the output csv file name.
    output_csv = "comments-updated-2_23_25.csv"

    # Build the pipeline and await for it to be done.
    pipeline = FilterComments(folder_path, api_key, output_csv, batch_size=20)
    await pipeline.run()

    # Close the classifier session.
    await pipeline.classifier.close()

if __name__ == '__main__':
    asyncio.run(main())
   