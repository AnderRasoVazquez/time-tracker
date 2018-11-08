from configparser import ConfigParser

config = ConfigParser()
config.read("timetracker.ini")

# TODO solucionar el padding de espacios
print(config.get("INFO", "activities").split(","))