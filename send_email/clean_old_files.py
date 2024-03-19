import os
import shutil
from datetime import datetime, timedelta

def delete_old_directories(path_prefix, days_old=7):
    """
    Deletes directories at a given path prefix if their suffix represents a date
    more than a specified number of days old.

    :param path_prefix: The prefix of the path to check directories for.
    :param days_old: Number of days to check the age of the directory.
    """
    # Ensure the path exists
    if not os.path.exists(path_prefix):
        print(f"Path {path_prefix} does not exist.")
        return
    
    # Get the current date
    current_date = datetime.now()
    
    # Loop through each item in the directory
    for item in os.listdir(path_prefix):
        full_path = os.path.join(path_prefix, item)
        
        # Check if the item is a directory
        if os.path.isdir(full_path):
            try:
                # Extract the date from the directory name
                date_str = item[-8:]
                dir_date = datetime.strptime(date_str, '%Y%m%d')
                
                # Calculate the age of the directory
                if current_date - dir_date > timedelta(days=days_old):
                    # Delete the directory if it's older than the specified number of days
                    shutil.rmtree(full_path)
                    print(f"Deleted {full_path}")
            except ValueError:
                # If the directory name does not end in a date, ignore it
                pass

# Example usage
if __name__ == "__main__":
    delete_old_directories('/Users/user/nwd_ig_crawler/sdc/PM')
    delete_old_directories('/Users/user/nwd_ig_crawler/scheduler/logs')
