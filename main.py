"""Main file."""
import random
import string
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')


from gi.repository import Adw, Gtk

from panels import default_apps, terminal

PANELS = [
    default_apps.DefaultApplications(),
    terminal.Terminal()
]

class MainWindow(Gtk.ApplicationWindow):
    """Main window for settings application."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.load_panels()
        self.load_stack()


        self.set_title(title="Settings")
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        leaflet = Adw.Leaflet.new()

        leaflet.append(self.get_navigation_pane())
        leaflet.append(Gtk.Separator.new(orientation=Gtk.Orientation.VERTICAL))
        
        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.append(self.stack)

        leaflet.append(box)

        self.set_child(child=leaflet)

    def load_panels(self):
        """Loads all the panels."""
        for panel in PANELS:
            panel.load_widget()

    def get_navigation_pane(self):
        """Returns navigation panel widget."""
        list_box = Gtk.ListBox.new()
        list_box.set_css_classes(["navigation-sidebar"])
        list_box.connect("row-activated", self.on_list_box_row_activated)

        for panel in PANELS:
            item = Gtk.ListBoxRow.new()
            item.set_name(panel.name)


            grid = Gtk.Grid.new()
            grid.set_column_spacing(12)
            grid.set_margin_top(12)
            grid.set_margin_bottom(12)
            grid.set_margin_start(6)
            grid.set_margin_end(6)

            label = Gtk.Label.new()
            label.set_text(panel.name)

            icon = Gtk.Image.new_from_icon_name(panel.icon)

            grid.attach(icon, 0, 0, 1, 1)
            grid.attach(label, 1, 0, 1, 1)

            item.set_child(child=grid)
            item.set_activatable(True)
            item.set_selectable(True)

            list_box.append(item)

        return list_box

    def load_stack(self):
        """Loads stack widget."""
        self.stack = Gtk.Stack.new()

        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        for panel in PANELS:
            self.stack.add_named(panel.widget, panel.name)

    def on_list_box_row_activated(self, _, row):
        """Handles list box row activation."""
        name = row.get_name()
        self.stack.get_child_by_name(name).show()
        self.stack.set_visible_child_name(name)

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
