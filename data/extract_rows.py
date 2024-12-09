import pandas as pd

# Load the CSV file
crime_data_file_path = 'data/crime_data.csv'

# Read the CSV file into a DataFrame
crime_data_full = pd.read_csv(crime_data_file_path)

# Extract the first 5% of rows
first_5_percent = crime_data_full.head(int(len(crime_data_full) * 0.05))

# Save the extracted DataFrame to a new CSV file
output_file_path = 'data/first_5_percent.csv'

# Save the DataFrame
first_5_percent.to_csv(output_file_path, index=False)

# Confirm the save operation
print(f"File saved at: {output_file_path}")
