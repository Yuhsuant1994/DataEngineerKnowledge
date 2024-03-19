import os
import csv

# File path
file_path = '/Users/user/nwd_ig_crawler/sdc/account_in_use.csv'

# Check if the file exists and delete it
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Deleted existing file: {file_path}")
else:
    print(f"No file found to delete: {file_path}")

# Create a new CSV file and add a header with 'user' column only
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['login'])  # Writing the header with 'login' column

print(f"Created new file with 'login' column: {file_path}")
