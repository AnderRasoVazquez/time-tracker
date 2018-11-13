import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib, Gio
from appconfig import TrackerConfig
from ui.main.widgets.header.headerbar import HeaderBar
from ui.main.widgets.forms.activity_info import ActivityGrid


class AppWindow(Gtk.ApplicationWindow):
    """Application's main window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = TrackerConfig()

        settings = Gio.Settings('com.github.anderrasovazquez.timetracker')
        settings.connect("changed::darkmode", self._on_darkmode_changed, self)

        self.set_resizable(False)

        if self._config.get_darkmode():
            settings_theme = Gtk.Settings.get_default()
            settings_theme.set_property("gtk-application-prefer-dark-theme", True)

        self.hb = HeaderBar()
        self.set_titlebar(self.hb)

        self.grid = ActivityGrid(self, self._config.get_activities())

        self.add(self.grid)

        self.show_all()
        self.grid.infobar.hide()
        self.grid.infobar_error.hide()

    def update_values(self, widget):
        # TODO una solucion para coger los valores de la actividad pero el csv no se updatearia
        print(widget.entry_activities.get_text())
        self.grid.update_values()

    def _on_darkmode_changed(self, settings, key, check_button):
        # TODO no va con settings, no lo llama si no es self.settings
        print(settings.get_boolean("darkmode"))
        print(self.settings.get_boolean("darkmode"))
