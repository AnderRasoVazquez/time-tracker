"""Handle app configuration."""
import os
from configparser import ConfigParser
from csv_manager import CSVManager


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
        CSVManager().create_if_not_exists(csv_path)
        return csv_path

    def _get_config_file_path(self):
        """Tries to read user config file at ~/.timetracker.ini, if it doesn't exist reads default config."""
        # TODO try reading home folder else use default config
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "timetracker.ini")

    def _parse_activities(self):
        """Returns a list of activities from config file."""
        activities = self._config.get("INFO", "activities").split(",")
        return [item.strip() for item in activities]
