"""This module handles the csv file operations."""
import os


class CSVManager(object):
    """Edits csv."""
    def __init__(self):
        pass

    def create_if_not_exists(self, csv_path):
        """Creates a csv if not exists."""
        dir_path = os.path.dirname(os.path.realpath(csv_path))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Created: " + dir_path)

        if not os.path.exists(csv_path):
            with open(csv_path, "w") as f:
                f.write("date,activity,time\n")
                print("Created: " + csv_path)

    def save_entry(self, csv_path, year, month, day, activity, hours):
        """Save a new entry to the csv."""
        # TODO try catch return false
        with open(csv_path, "a") as f:
            line = "{}-{}-{},{},{}\n".format(year, month, day, activity, hours)
            f.write(line)
            print("CSV file updated: ", line)

        return True
