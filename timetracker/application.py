import gi
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Gio
from ui.main.window import AppWindow
from appconfig import TrackerConfig
from ui.settings.window import SettingsWindow


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.github.anderrasovazquez.timetracker", **kwargs)
        self.config = TrackerConfig()
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("edit_csv", None)
        action.connect("activate", self.on_edit_csv)
        self.add_action(action)

        action = Gio.SimpleAction.new("settings", None)
        action.connect("activate", self.on_settings)
        self.add_action(action)

        action = Gio.SimpleAction.new("show_data", None)
        action.connect("activate", self.on_show_data)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title="TimeTracker")

        self.window.present()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        # about_dialog.present()

        # lists of authors and documenters (will be used later)
        authors = ["Ander Raso Vazquez"]
        documenters = ["Ander Raso Vazquez"]

        # we fill in the aboutdialog
        about_dialog.set_program_name("Time Tracker")
        # about_dialog.set_copyright(
        #     "Copyright \xc2\xa9 2012 GNOME Documentation Team")
        about_dialog.set_authors(authors)
        about_dialog.set_documenters(documenters)
        about_dialog.set_website("https://github.com/AnderRasoVazquez/time-tracker")
        about_dialog.set_website_label("GitHub - TimeTracker")

        # we do not want to show the title, which by default would be "About AboutDialog Example"
        # we have to reset the title of the messagedialog window after setting
        # the program name
        about_dialog.set_title("")

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        about_dialog.connect("response", self.on_close)
        # show the aboutdialog
        about_dialog.show()

    def on_close(self, action, parameter):
        # destroy the aboutdialog
        action.destroy()

    def on_quit(self, action, param):
        self.quit()

    def on_edit_csv(self, action, param):
        subprocess.call(["xdg-open", TrackerConfig().get_csv_path()])

    def on_settings(self, action, param):
        settings_window = SettingsWindow(self.window)
        settings_window.connect("destroy", self.window.update_values)

    def update_values(self, widget):
        self.window.update_values()

    def on_show_data(self, action, param):
        print("show data clicked - not implemented yet")

