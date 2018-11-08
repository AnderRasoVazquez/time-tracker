from configparser import ConfigParser

import os


class TrackerConfig(object):
    """Reads applications configuration."""

    def __init__(self):
        self._config_file = self._get_config_file_path()

        self._config = ConfigParser()
        self._config.read(self._config_file)

        # TODO try catch for readings
        self.darkmode = self._config.getboolean("STYLE", "darkmode")
        self.activities = self._parse_activities()
        self.csv_path = self._get_csv_path()

    def _get_csv_path(self):
        """Returns a valid path for the csv file, if it doesn't exist creates it."""
        csv_path = self._config.get("PATHS", "csv_path")
        dir_path = os.path.dirname(os.path.realpath(csv_path))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Created: " + dir_path)

        if not os.path.exists(csv_path):
            with open(csv_path, "w") as f:
                f.write("year,month,day,activity,hours\n")
                print("Created: " + csv_path)

        return csv_path

    def _get_config_file_path(self):
        """Tries to read user config file at ~/.timetracker.ini, if it doesn't exist reads default config."""
        # TODO try catch for file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "timetracker.ini")

    def _parse_activities(self):
        """Returns a list of activities from config file."""
        activities = self._config.get("INFO", "activities").split(",")
        return [item.strip() for item in activities]
