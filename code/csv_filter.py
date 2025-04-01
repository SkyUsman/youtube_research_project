import csv
import os
import glob
from dotenv import load_dotenv
import pandas as pd

def filter_csv_files(input_directory: str, output_directory: str):
    '''
    Filter data already within a CSV.
    This is much faster an uses new tech as opposed to the previous script.
    Input directory grabs all the csv's and output directory is where the new csv's will be housed.
    This can be incorportated into the original filter, but if forgotten after before llm classification, this script can help.

    Author: Ameer Ghazal
    '''
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Get list of all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_directory, "*.csv"))
    
    for file_path in csv_files:
        # Get the filename without the directory path
        file_name = os.path.basename(file_path)
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Filter rows where likes > 50 and author is not null/empty
        filtered_df = df[(df['likes'] > 150) & (df['author'].notna()) & (df['author'] != '')]
        
        # Write the filtered data to a new CSV file in the output directory
        output_path = os.path.join(output_directory, file_name)
        filtered_df.to_csv(output_path, index=False)
        
if __name__ == "__main__":
    # Load enviorment variables.
    load_dotenv()

    # Specify your input and output directories
    input_dir = os.getenv('INPUT_CSV_DIR')
    output_dir = os.getenv('OUTPUT_CSV_DIR')
    
    # Run the functions.
    filter_csv_files(input_dir, output_dir)