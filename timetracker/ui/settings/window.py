"""Settings window."""

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from appconfig import TrackerConfig


class SettingsWindow(Gtk.Window):
    def __init__(self, parent):
        super().__init__()
        self.main_window = parent
        self.set_transient_for(self.main_window)
        self.set_modal(True)
        self.set_border_width(30)

        self._config = TrackerConfig()

        if self._config.get_darkmode():
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)

        self.hb = Gtk.HeaderBar()
        self.hb.set_title("Settings")
        self.hb.set_show_close_button(True)
        self.set_titlebar(self.hb)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)

        self.checkbutton_darkmode = Gtk.CheckButton("Use dark theme variant")
        self.checkbutton_darkmode.set_active(self._config.get_darkmode())
        self.label_activities = Gtk.Label("Activities")
        self.label_activities.set_tooltip_text("Separate the activities with a comma")
        self.label_activities.set_xalign(1)
        self.entry_activities = Gtk.Entry()
        self.entry_activities.set_text(", ".join(self._config.get_activities()))
        self.entry_activities.set_hexpand(True)
        self.entry_activities.connect("changed", self._on_entry_activities_changed)

        self.label_csv_path = Gtk.Label("Data file path")
        self.label_csv_path.set_tooltip_text("Your activity log is stored here")
        self.entry_csv_path = Gtk.Entry()
        self.entry_csv_path.set_text(self._config.get_csv_path())
        self.entry_csv_path.connect("changed", self._on_entry_csv_path_changed)
        # self.button_file_chooser = Gtk.Button.new_from_icon_name("open-menu", Gtk.IconSize.BUTTON)
        # self.button_file_chooser = Gtk.Button(label="select file")
        # self.button_file_chooser = Gtk.FileChooserButton()

        self.grid.set_hexpand(True)
        self.grid.attach(self.checkbutton_darkmode, 0, 0, 2, 1)
        self.grid.attach(self.label_activities, 0, 1, 1, 1)
        self.grid.attach(self.entry_activities, 1, 1, 1, 1)
        self.grid.attach(self.label_csv_path, 0, 2, 1, 1)
        self.grid.attach(self.entry_csv_path, 1, 2, 1, 1)
        # self.grid.attach(self.button_file_chooser, 2, 2, 1, 1)

        self.add(self.grid)

        self.checkbutton_darkmode.connect("toggled", self._on_checkbutton_darkmode_toggled)

        self.show_all()

    def _on_entry_activities_changed(self, widget):
        self._config.set_activities(self.entry_activities.get_text())

    def _on_entry_csv_path_changed(self, widget):
        self._config.set_csv_path(self.entry_csv_path.get_text())

    def _on_checkbutton_darkmode_toggled(self, widget):
        darkmode = self.checkbutton_darkmode.get_active()
        self._config.set_darkmode(darkmode)
        settings = Gtk.Settings.get_default()
        if darkmode:
            settings.set_property("gtk-application-prefer-dark-theme", True)
        else:
            settings.set_property("gtk-application-prefer-dark-theme", False)


if __name__ == '__main__':
    SettingsWindow()
    Gtk.main()


