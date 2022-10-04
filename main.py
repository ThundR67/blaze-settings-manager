"""Main file."""
import random
import string
import sys

import gi
from gi.repository import Adw, Gtk

from panels import default_apps


gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')


PANELS = [default_apps.DefaultApplications()]

class MainWindow(Gtk.ApplicationWindow):
    """Main window for settings application."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title="Settings")
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        leaflet = Adw.Leaflet.new()
        leaflet.append(self.get_navigation_pane())
        leaflet.append(self.get_stack())

        self.set_child(child=leaflet)

    def get_navigation_pane(self):
        """Returns navigation panel widget."""
        list_box = Gtk.ListBox.new()

        for panel in PANELS:
            item = Gtk.ListBoxRow.new()

            grid = Gtk.Grid.new()
            grid.set_column_spacing(12)
            grid.set_margin_top(6)
            grid.set_margin_bottom(6)
            grid.set_margin_start(12)
            grid.set_margin_end(12)

            label = Gtk.Label.new()
            label.set_text(panel.name)

            icon = Gtk.Image.new_from_icon_name(panel.icon)

            grid.attach(icon, 0, 0, 1, 1)
            grid.attach(label, 1, 0, 1, 1)

            item.set_child(child=grid)
            list_box.append(item)
        
        return list_box

    def get_stack(self):
        """Returns stack widget."""
        stack = Gtk.Stack.new()

        for panel in PANELS:
            stack.add_titled(panel.get_widget(), panel.name, panel.name)

        return stack


class Application(Adw.Application):
    """Main application class for setttins application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        """Callback for application activation."""
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == '__main__':
    app = Application(application_id=random.choices(string.ascii_lowercase))
    app.run(sys.argv)
