import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from appconfig import TrackerConfig
from ui.main_window.widgets.header.headerbar import HeaderBar
from ui.main_window.widgets.forms.activity_info import ActivityGrid


class AppWindow(Gtk.ApplicationWindow):
    """Application's main window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = TrackerConfig()
        self.set_border_width(10)
        self.set_resizable(False)

        if self._config.darkmode:
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)

        self.hb = HeaderBar()
        self.set_titlebar(self.hb)

        self.grid = ActivityGrid(self._config.activities)
        self.add(self.grid)

        self.show_all()



