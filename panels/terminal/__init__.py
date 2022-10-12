"""Panel to customize the terminal."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk


class Terminal:
    """Panel to customize terminal."""
    def __init__(self):
        self.name = "Terminal"
        self.icon = "org.gnome.Settings-wacom-symbolic"

    def load_widget(self):
        """Loads widget for panel."""
        self.widget = Adw.Bin.new()

        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.START)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(24)
        box.set_margin_end(24)

        grid = Gtk.Grid.new()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_valign(Gtk.Align.FILL)
        grid.set_halign(Gtk.Align.FILL)

        box.append(grid)
        self.widget.set_child(box)
