import gi
import random
import os

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio
from definitions import ROOT_DIR
from colors import Colors


class HeaderBar(Gtk.HeaderBar):
    """Main window's header."""
    def __init__(self):
        super().__init__()

        quotes = [
                  # "Time is an illusion",
                  # "No time to explain",
                  _("Focus on what matters"),
                  # "Life is short",
                  # "Lazy... or efficient?"
        ]

        rand_quote = quotes[random.randint(0, len(quotes) - 1)]

        self.set_show_close_button(True)
        self.props.title = "Time Tracker"
        self.props.subtitle = rand_quote

        self.button_menu = Gtk.MenuButton()
        self.button_menu.set_tooltip_text(_("Open menu"))
        self.button_menu.set_image(Gtk.Image.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR))
        self.pack_end(self.button_menu)

        builder = Gtk.Builder.new_from_file(os.path.join(ROOT_DIR, "appmenu.xml"))
        menu_old = builder.get_object("app-menu")

        menu = Gio.Menu()
        menu.append("Item 1", "app.quit")
        menu2 = Gio.Menu()
        menu2.append("Otro", "app.quit")
        menu.append_submenu("Submenu", menu2)
        # item = Gio.MenuItem.new("Item 1", "app.quit")
        item2 = Gio.MenuItem()
        item2.set_label("prueba2")
        item3 = Gio.MenuItem()
        item3.set_label("prueba3")
        # menu.append_item(item)
        menu.append_item(item2)
        menu.append_item(item3)

        popover = Gtk.Popover.new_from_model(self.button_menu, menu_old)

        self.button_menu.set_popover(popover)
        self.change_color()

    def change_color(self):
        # There are better methods to define CSS variables, but this is an example.
        stylesheet = """
                    @define-color colorPrimary """ + Colors.primary_color + """;
                    @define-color textColorPrimary """ + Colors.primary_text_color + """;
                    @define-color textColorPrimaryShadow """ + Colors.primary_text_shadow_color + """;
                """;

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(bytes(stylesheet.encode()))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

