import gi
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)


class MyWindow(Gtk.Window):
    """Application's main window."""

    def __init__(self):
        Gtk.Window.__init__(self, title="Time Tracker")

        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.add(self.grid)

        activities = ["Choose an activity", "Desarrollo", "Documentacion"]
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
        self.button_save.connect("clicked", self.on_button_save_clicked)
        self.button_save.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        # add widgets
        self.grid.attach(self.combo_activity, 0, 0, 2, 1)
        self.grid.attach(self.calendar, 0, 1, 2, 1)
        self.grid.attach(self.box, 0, 2, 2, 1)
        self.grid.attach(self.button_save, 0, 3, 2, 1)

    def on_button_save_clicked(self, widget):
        """Save entry to csv."""
        print("Hello World")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
