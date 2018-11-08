import gi
import datetime
import random
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Notify, Gio
from config import TrackerConfig


class TrackerWindow(Gtk.Window):
    """Application's main window."""

    def __init__(self):
        Gtk.Window.__init__(self, title="Time Tracker")
        self.connect("destroy", Gtk.main_quit)
        self._config = TrackerConfig()

        quotes = ["Time is an illusion",
                  "No time to explain",
                  "Focus on what matters",
                  "Life is short",
                  "Lazy... or efficient?"]

        rand_quote = quotes[random.randint(0, len(quotes) - 1)]

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Time Tracker"
        self.hb.props.subtitle = rand_quote

        self.set_titlebar(self.hb)

        self.button_edit = Gtk.Button()
        self.button_edit.set_tooltip_text("Open CSV file with your default editor")
        icon = Gio.ThemedIcon(name="text-editor")
        # icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_edit.add(image)
        self.button_edit.connect("clicked", self._on_button_edit_clicked)
        self.hb.pack_end(self.button_edit)

        if self._config.darkmode:
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)

        self.set_border_width(10)
        self.set_resizable(False)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.add(self.grid)

        activities = ["Choose an activity"] + self._config.activities
        self.combo_activity = Gtk.ComboBoxText()

        for item in activities:
            self.combo_activity.append_text(item)

        self.combo_activity.set_active(0)

        # create a new calendar
        date = datetime.date.today()
        self.calendar = Gtk.Calendar()
        self.calendar.select_month(date.month - 1, date.year)
        self.calendar.select_day(date.day)

        self.box = Gtk.Box(spacing=6)

        self.label_hours = Gtk.Label("Hours worked")

        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.spinbutton_hours = Gtk.SpinButton()
        self.spinbutton_hours.set_adjustment(adjustment)

        self.box.pack_start(self.label_hours, True, True, 0)
        self.box.pack_end(self.spinbutton_hours, True, True, 0)

        self.button_save = Gtk.Button(label="Save entry")
        self.button_save.connect("clicked", self._on_button_save_clicked)
        self.button_save.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        # add widgets
        self.grid.attach(self.combo_activity, 0, 0, 2, 1)
        self.grid.attach(self.calendar, 0, 1, 2, 1)
        self.grid.attach(self.box, 0, 2, 2, 1)
        self.grid.attach(self.button_save, 0, 3, 2, 1)

        self.show_all()

    def _on_button_edit_clicked(self, widget):
        filepath = self._config.csv_path
        # TODO make it multiplatform
        # if sys.platform.startswith('darwin'):
        #     subprocess.call(('open', filepath))
        # elif os.name == 'nt': # For Windows
        #     os.startfile(filepath)
        # elif os.name == 'posix': # For Linux, Mac, etc.
        #     subprocess.call(('xdg-open', filepath))

        subprocess.call(('xdg-open', filepath))

    def _on_button_save_clicked(self, widget):
        """Save entry to csv."""
        # get data
        date = self.calendar.get_date()
        year = date.year
        month = date.month + 1  # months start at 0 in Gtk.Calendar
        day = date.day
        activity_id = self.combo_activity.get_active()
        hours_worked = self.spinbutton_hours.get_value()
        activity_text = self.combo_activity.get_active_text()

        # TODO handle errors with a dialog
        if activity_id == 0:
            self._notify("Error", "Choose an activity before saving the entry.", icon="dialog-error")
            return
        elif hours_worked <= 0:
            self._notify("Error", "Working hours must be gerater than 0.", icon="dialog-error")
            return

        self._save_entry(year, month, day, activity_text, hours_worked)

    def _save_entry(self, year, month, day, activity, hours):
        """Save a new entry to the csv."""
        # TODO create a csv manager
        with open(self._config.csv_path, "a") as f:
            line = "{},{},{},{},{}\n".format(year, month, day, activity, hours)
            f.write(line)
            print("CSV file updated: ", line)
            self._notify("Entry saved succesfully", "PATH: " + self._config.csv_path)

    def _notify(self, summary, body=None, icon="dialog-information"):
        """Notify when an entry is saved."""
        Notify.init("Time Tracker")

        # Create the notification object
        notification = Notify.Notification.new(
            summary,
            body,  # Optional
            icon  # dialog-information, dialog-warn, dialog-error
        )
        notification.show()
