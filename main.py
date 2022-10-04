"""Main file."""
import random
import string
import sys

# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Adw.Flap()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Gio, Gtk
from gi.repository import Adw


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pages = [["Default Applications", "org.gnome.Settings-default-apps-symbolic"]]

        self.set_title(title="Settings")
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        leaflet = Adw.Leaflet.new()
        leaflet.append(self.get_navigation_pane())
  
        self.set_child(child=leaflet)

    def get_navigation_pane(self):
        list_box = Gtk.ListBox.new()

        for name, icon in self.pages: 
            item = Gtk.ListBoxRow.new()

            grid = Gtk.Grid.new()
            grid.set_column_spacing(12)
            grid.set_margin_top(6)
            grid.set_margin_bottom(6)
            grid.set_margin_start(12)
            grid.set_margin_end(12)

            label = Gtk.Label.new()
            label.set_text(name)

            icon = Gtk.Image.new_from_icon_name(icon)

            grid.attach(icon, 0, 0, 1, 1)
            grid.attach(label, 1, 0, 1, 1)
        

        item.set_child(grid)
        list_box.append(item)
        return list_box



class Application(Adw.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

app = Application(application_id=random.choices(string.ascii_lowercase))
app.run(sys.argv)