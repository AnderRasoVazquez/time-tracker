import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.window import TrackerWindow


def main():
    TrackerWindow()
    Gtk.main()


if __name__ == '__main__':
    main()
