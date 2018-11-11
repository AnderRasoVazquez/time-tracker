"""Settings window."""

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from appconfig import TrackerConfig


class SettingsWindow(Gtk.Window):
    def __init__(self):
        super().__init__()


