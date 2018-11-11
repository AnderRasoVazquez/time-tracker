import gi
import random

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk


# TODO manage the colors better
class Colors:
    primary_color = "rgba(100, 85, 82, 1)"
    primary_text_color = "#EEEDEC"
    primary_text_shadow_color = "#53433F"


class HeaderBar(Gtk.HeaderBar):
    """Main window's header."""
    def __init__(self):
        super().__init__()

        quotes = ["Time is an illusion",
                  "No time to explain",
                  "Focus on what matters",
                  "Life is short",
                  "Lazy... or efficient?"]

        rand_quote = quotes[random.randint(0, len(quotes) - 1)]

        self.set_show_close_button(True)
        self.props.title = "Time Tracker"
        self.props.subtitle = rand_quote

        self.button_menu = Gtk.MenuButton()
        self.button_menu.set_tooltip_text("Open menu")
        self.button_menu.set_image(Gtk.Image.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR))
        self.pack_end(self.button_menu)

        builder = Gtk.Builder.new_from_file("appmenu.xml")
        menu = builder.get_object("app-menu")
        popover = Gtk.Popover.new_from_model(self.button_menu, menu)

        self.button_menu.set_popover(popover)
        self.change_color()

    def change_color(self):
        # There are better methods to define CSS variables, but this is an example.
        stylesheet = """
                    @define-color colorPrimary """ + "#452981" + """;
                    @define-color textColorPrimary """ + Colors.primary_text_color + """;
                    @define-color textColorPrimaryShadow """ + Colors.primary_text_shadow_color + """;
                """;

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(bytes(stylesheet.encode()))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

