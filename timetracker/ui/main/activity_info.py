import gi
import datetime

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Notify, GLib
from csv_manager import CSVManager
from appconfig import TrackerConfig


class ActivityGrid(Gtk.Grid):
    """Activity info form."""
    def __init__(self, parent, activities):
        super().__init__()
        self.parent = parent
        self.set_row_spacing(10)
        self.set_border_width(10)

        self.combo_activity = Gtk.ComboBoxText()
        self._set_activities(activities)
        self.combo_activity.connect("changed", self._on_form_updated)

        # create a new calendar
        date = datetime.date.today()
        self.calendar = Gtk.Calendar()
        self.calendar.select_month(date.month - 1, date.year)
        self.calendar.select_day(date.day)

        self.box = Gtk.Box(spacing=6)

        self.label_time = Gtk.Label(_("Time worked"))
        self.label_time.set_tooltip_text(_("Minutes, hours, days... What you prefer."))

        # TODO get time increase
        adjustment = Gtk.Adjustment(0, 0, 24*60, 1, 0, 0)
        self.spinbutton_time = Gtk.SpinButton()
        self.spinbutton_time.set_adjustment(adjustment)
        self.spinbutton_time.connect("changed", self._on_form_updated)

        self.box.pack_start(self.label_time, True, True, 0)
        self.box.pack_end(self.spinbutton_time, True, True, 0)

        self.button_save = Gtk.Button(label=_("Save entry"))
        self.button_save.set_always_show_image(True)
        self.button_save.connect("clicked", self._on_button_save_clicked)
        self.button_save.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.button_save.set_sensitive(False)
        self.button_save.set_tooltip_text(_("Choose an activity and set the minutes before saving"))
        self.button_save.set_image(Gtk.Image.new_from_icon_name("accessories-text-editor-symbolic", Gtk.IconSize.BUTTON))

        # add widgets
        self.attach(self.combo_activity, 0, 0, 2, 1)
        self.attach(self.calendar, 0, 1, 2, 1)
        self.attach(self.box, 0, 2, 2, 1)
        self.attach(self.button_save, 0, 3, 2, 1)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.INFO)
        self.infobar.get_content_area().add(Gtk.Label(_("New entry saved")))
        # self.infobar.set_show_close_button(True)
        self.infobar.connect("response", self._on_infobar_response)
        self.attach(self.infobar, 0, 4, 2, 1)

        self.infobar_error = Gtk.InfoBar()
        self.infobar_error.set_message_type(Gtk.MessageType.ERROR)
        self.infobar_error.get_content_area().add(Gtk.Label(_("Error saving entry")))
        self.infobar_error.set_show_close_button(True)
        self.infobar_error.connect("response", self._on_infobar_response)
        self.attach(self.infobar_error, 0, 5, 2, 1)

        self.infobar.hide()

    def update_values(self):
        self.combo_activity.remove_all()
        t = TrackerConfig()
        activities = t.get_activities()
        self._set_activities(activities)

    def _set_activities(self, activities):
        activity_list = [_("Choose an activity")] + activities
        for item in activity_list:
            self.combo_activity.append_text(item)
        self.combo_activity.set_active(0)


    def _on_infobar_response(self, infobar, respose_id):
        self.infobar.hide()
        self.infobar_error.hide()
        self.button_save.show()

    def _on_form_updated(self, widget):
        activity_id = self.combo_activity.get_active()
        time_worked = self.spinbutton_time.get_value()
        if activity_id != 0 and time_worked > 0:
            self.button_save.set_sensitive(True)
        else:
            self.button_save.set_sensitive(False)

    def _on_button_save_clicked(self, widget):
        """Save entry to csv."""
        # get data
        date = self.calendar.get_date()
        year = date.year
        month = date.month + 1  # months start at 0 in Gtk.Calendar
        day = date.day
        activity_id = self.combo_activity.get_active()
        time_worked = self.spinbutton_time.get_value()
        activity_text = self.combo_activity.get_active_text()

        self._save_entry(year, month, day, activity_text, time_worked)

    def _save_entry(self, year, month, day, activity, time):
        """Save a new entry to the csv."""
        csv_path = TrackerConfig().get_csv_path()
        if CSVManager().save_entry(csv_path, year, month, day, activity, time):
            self.button_save.hide()
            self.infobar.show()
            GLib.timeout_add(1500, self._on_timeout, None)
        else:
            self.button_save.hide()
            self.infobar_error.show()

    def _on_timeout(self, userdata):
        self.button_save.show()
        self.infobar.hide()
        # self.button_save.set_label("Save entry")

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
