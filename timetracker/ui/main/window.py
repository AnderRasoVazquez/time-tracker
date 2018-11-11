import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib
from appconfig import TrackerConfig
from ui.main.widgets.header.headerbar import HeaderBar
from ui.main.widgets.forms.activity_info import ActivityGrid


class AppWindow(Gtk.ApplicationWindow):
    """Application's main window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = TrackerConfig()
        self.set_resizable(False)

        if self._config.darkmode:
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)

        self.hb = HeaderBar()
        self.set_titlebar(self.hb)

        self.grid = ActivityGrid(self, self._config.activities)

        self.add(self.grid)

        self.show_all()
        self.grid.infobar.hide()
        self.grid.infobar_error.hide()
