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

        stack = Gtk.Stack.new()
        leaflet.append(stack)

        box_page_1 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        stack.add_titled(child=box_page_1, name='pagina1', title='Página 1')

        label_page_1 = Gtk.Label.new(str='Página 1')
        label_page_1.set_halign(align=Gtk.Align.CENTER)
        label_page_1.set_valign(align=Gtk.Align.CENTER)
        label_page_1.set_hexpand(expand=True)
        label_page_1.set_vexpand(expand=True)
        box_page_1.append(child=label_page_1)

        self.set_child(child=leaflet)

    def get_navigation_pane(self):
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


        item.set_child(grid)
        list_box.append(item)
        return list_box


class Application(Adw.Application):
    """Main application class for setttins application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    app = Application(application_id=random.choices(string.ascii_lowercase))
    app.run(sys.argv)
