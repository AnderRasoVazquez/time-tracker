import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio
from colors import Colors


class HeaderBar(Gtk.HeaderBar):
    """Main window's header."""
    def __init__(self):
        super().__init__()

        self.set_show_close_button(True)
        self.props.title = _("Time Tracker")
        self.props.subtitle = _("Focus on what matters")

        self.button_menu = Gtk.MenuButton()
        self.button_menu.set_tooltip_text(_("Open menu"))
        self.button_menu.set_image(Gtk.Image.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR))
        self.pack_end(self.button_menu)

        popover = Gtk.Popover.new_from_model(self.button_menu, self._build_app_menu())

        self.button_menu.set_popover(popover)
        self.change_color()

    def _build_app_menu(self):
        menu = Gio.Menu()
        menu.append(_("Edit CSV file"), "app.edit_csv")
        menu.append(_("Open Data Analyzer"), "app.show_data")

        menu_settings = Gio.Menu()
        menu_settings.append(_("Settings"), "app.settings")
        menu.append_section(None, menu_settings)

        menu_close = Gio.Menu()
        menu_close.append(_("About"), "app.about")
        menu_close.append(_("Quit"), "app.quit")
        menu.append_section(None, menu_close)
        return menu

    def change_color(self):
        # TODO handle better CSS stylesheet
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

