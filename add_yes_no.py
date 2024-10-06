import pandas as pd

# Load the existing CSV
csv_file_path = 'ahmed_ameer_combined_dataset.csv'  # Replace with the path to your actual CSV file
df = pd.read_csv(csv_file_path)

# Add 'yes_count', 'no_count', and 'skip_count' columns and initialize them to 0
df['yes_count'] = 0
df['no_count'] = 0
df['skip_count'] = 0

# Save the updated CSV
updated_csv_file_path = 'ahmed_ameer_combined_dataset_updated.csv'  # Replace with desired output file path
df.to_csv(updated_csv_file_path, index=False)

print(f"CSV updated and saved at: {updated_csv_file_path}")
