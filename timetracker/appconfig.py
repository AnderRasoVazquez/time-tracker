"""Handle app configuration."""
import os

from gi.repository import Gio, GLib
from csv_manager import CSVManager
from configparser import ConfigParser


class GsettingsConfig(object):
    """Uses gsettings schemas as configuration."""
    # TODO setting and then retrieving from other window doesn't work
    def __init__(self):
        # Borg.__init__(self)
        self.settings = Gio.Settings('com.github.anderrasovazquez.timetracker')

    def get_darkmode(self):
        return self.settings.get_boolean("darkmode")

    def set_darkmode(self, value):
        self.settings.set_boolean("darkmode", value)

    def get_csv_path(self):
        """Returns a valid path for the csv file, if it doesn't exist creates it."""
        csv_path = self.settings.get_string("csv-path")
        csv_path = os.path.expanduser(csv_path)
        CSVManager().create_if_not_exists(csv_path)
        return csv_path

    def set_csv_path(self, csv_path):
        # TODO y si el archivo no es correcto?
        self.settings.set_string("csv-path", csv_path)

    def get_activities(self):
        """Returns a list of activities from config file."""
        activities = [item.strip() for item in self.settings.get_value("activities")]
        activities = list(set(activities))
        return activities

    def set_activities(self, text):
        activities = self._parse_activities(text)
        self.settings.set_value("activities", GLib.Variant('as', activities))
        return activities

    def _parse_activities(self, text):
        activities = text.split(",")
        activities = [item.strip() for item in activities]
        activities = [item for item in activities if item]
        return list(set(activities))


class IniConfig(object):
    """Uses configparses """

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.dir_path, "timetracker.ini")
        # self.config_path = "/home/ander/github/TimeTracker/timetracker/timetracker.ini"
        self._config = ConfigParser()
        self._read_config()

    def _read_config(self):
        self._config.read(self.config_path)

    def get_darkmode(self):
        self._read_config()
        return self._config["STYLE"].getboolean("darkmode")

    def set_darkmode(self, value):
        self._config["STYLE"]["darkmode"] = str(value)
        self._write_config()

    def _write_config(self):
        with open(self.config_path, 'w') as configfile:
            self._config.write(configfile)

    def get_csv_path(self):
        """Returns a valid path for the csv file, if it doesn't exist creates it."""
        self._read_config()
        csv_path = self._config["PATHS"]["csv_path"]
        csv_path = os.path.expanduser(csv_path)
        CSVManager().create_if_not_exists(csv_path)
        return csv_path

    def set_csv_path(self, csv_path):
        # TODO y si el archivo no es correcto?
        self._config["PATHS"]["csv_path"] = csv_path
        self._write_config()

    def get_activities(self):
        """Returns a list of activities from config file."""
        self._read_config()
        activities = self._parse_activities(self._config["INFO"]["activities"])
        return activities

    def set_activities(self, text):
        activities = self._parse_activities(text)
        activities = ", ".join(activities)
        self._config["INFO"]["activities"] = activities
        self._write_config()

    def _parse_activities(self, text):
        activities = text.split(",")
        activities = [item.strip() for item in activities]
        activities = [item for item in activities if item]
        activities = list(set(activities))
        return sorted(activities)


class TrackerConfig(object):
    """Reads applications configuration."""
    def __init__(self, backend="iniconfig"):
        if backend == "gsettings":
            self._config = GsettingsConfig()
        elif backend == "iniconfig":
            self._config = IniConfig()
        else:
            exit("That config mode doesn't exist.")

    def get_darkmode(self):
        return self._config.get_darkmode()

    def set_darkmode(self, value):
        self._config.set_darkmode(value)

    def get_csv_path(self):
        """Returns a valid path for the csv file, if it doesn't exist creates it."""
        return self._config.get_csv_path()

    def set_csv_path(self, csv_path):
        # TODO y si el archivo no es correcto?
        self._config.set_csv_path(csv_path)

    def get_activities(self):
        """Returns a list of activities from config file."""
        return self._config.get_activities()

    def set_activities(self, text):
        return self._config.set_activities(text)

