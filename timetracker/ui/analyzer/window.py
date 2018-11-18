import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')

from gi.repository import Gtk, Vte, Gio, GLib
from appconfig import TrackerConfig
from plot.heatmap import HeatMap
from plot.bar import TotalHoursBar


class AnalyzerWindow(Gtk.Window):
    """Window for the data analyzer."""
    def __init__(self):
        super().__init__()
        executable_path = self._get_executable_path()
        self._config = TrackerConfig()
        csv_dir = os.path.dirname(self._config.get_csv_path())
        self.terminal = Vte.Terminal()
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            csv_dir,
            [executable_path],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
        self.terminal.connect("child-exited", self._on_terminal_exit)

        self.hb = Gtk.HeaderBar()
        self.hb.set_title(_("Data Analyzer"))
        self.hb.set_subtitle(_("Learn everything about your data"))
        self.hb.set_show_close_button(True)
        self.set_titlebar(self.hb)

        self.button_menu = Gtk.MenuButton()
        self.button_menu.set_tooltip_text("Open menu")
        self.button_menu.set_image(Gtk.Image.new_from_icon_name("application-vnd.oasis.opendocument.chart", Gtk.IconSize.LARGE_TOOLBAR))
        self.hb.pack_end(self.button_menu)

        popover = Gtk.Popover.new_from_model(self.button_menu, self._build_app_menu())

        self.button_menu.set_popover(popover)

        self.add(self.terminal)

        self.action_group = Gio.SimpleActionGroup()
        self.insert_action_group("analyzer", self.action_group)

        self._set_actions()
        self.show_all()

    def _get_executable_path(self):
        ipython3_path = os.path.expanduser("~/.local/bin/ipython3")
        if os.path.exists(ipython3_path):
            return ipython3_path
        else:
            python3_path = "/usr/bin/python3"
            return python3_path

    def _build_app_menu(self):
        menu = Gio.Menu()

        submenu_terminal = Gio.Menu()
        submenu_terminal.append(_("Load DataFrame"), "analyzer.load_dataframe")
        submenu_terminal.append(_("Help"), "analyzer.help")

        menu_heatmap = Gio.Menu()
        menu_heatmap.append(_("Daily"), "analyzer.heatmap_daily")
        menu_heatmap.append(_("Weekly"), "analyzer.heatmap_weekly")
        menu_heatmap.append(_("Monthly"), "analyzer.heatmap_monthly")
        menu_heatmap.append(_("Yearly"), "analyzer.heatmap_yearly")

        menu_bars = Gio.Menu()
        menu_bars.append(_("Activity hour count"), "analyzer.bar_hour_count")
        # menu_bars.append(_("Real VS Expected hour count"), "analyzer.bar_real_vs_expected")

        menu_plots = Gio.Menu()
        menu_plots.append_submenu(_("Heatmap"), menu_heatmap)
        menu_plots.append_submenu(_("Bars"), menu_bars)

        # menu_report = Gio.Menu()
        # menu_report.append(_("Show full report"), "analyzer.show_data")

        menu_close = Gio.Menu()
        menu_close.append(_("Quit"), "analyzer.quit")

        # order menu
        menu.append_submenu(_("Terminal"), submenu_terminal)
        menu.append_submenu(_("Plots"), menu_plots)
        # menu.append_section(None, menu_report)
        menu.append_section(None, menu_close)

        return menu

    def _set_actions(self):
        self._add_action("load_dataframe", self._on_load_dataframe)
        self._add_action("help", self._on_help)
        self._add_action("quit", lambda *args: self.destroy())
        self._add_action("heatmap_daily", self._on_heatmap_daily)
        self._add_action("heatmap_weekly", self._on_heatmap_weekly)
        self._add_action("heatmap_monthly", self._on_heatmap_monthly)
        self._add_action("heatmap_yearly", self._on_heatmap_yearly)
        self._add_action("bar_hour_count", self._on_bar_hour_count)
        self._add_action("bar_real_vs_expected", self._on_bar_real_vs_expected)
        self._add_action("show_data", self._on_show_data)

    def _on_heatmap_daily(self, action, param):
        HeatMap(self._config.get_csv_path()).create_dayly()

    def _on_heatmap_weekly(self, action, param):
        HeatMap(self._config.get_csv_path()).create_weekly()

    def _on_heatmap_monthly(self, action, param):
        HeatMap(self._config.get_csv_path()).create_monthly()

    def _on_heatmap_yearly(self, action, param):
        HeatMap(self._config.get_csv_path()).create_yearly()

    def _on_bar_hour_count(self, action, param):
        TotalHoursBar(self._config.get_csv_path()).create()

    def _on_bar_real_vs_expected(self, action, param):
        pass

    def _on_show_data(self, action, param):
        pass

    def _add_action(self, action_name, func, signal="activate"):
        action = Gio.SimpleAction.new(action_name, None)
        action.connect(signal, func)
        self.action_group.add_action(action)

    def _on_help(self, action, param):
        command = "?\n"
        self.send_command(command)

    def _on_load_dataframe(self, action, param):
        command = "import pandas as pd\n" + \
                  "import matplotlib.pyplot as plt\n" + \
                  "df = pd.read_csv('" + self._config.get_csv_path() + "')\n"
        self.send_command(command)

    def _on_terminal_exit(self, *args):
        self.destroy()

    def send_command(self, command):
        length = len(command)
        self.terminal.feed_child(command, length)
