"""Panel to customize default applications."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk


class DefaultApplications:
    """Panel to customize default applications."""
    def __init__(self):
        self.name = "Default Applications"
        self.icon = "org.gnome.Settings-default-apps-symbolic"

    def get_widget(self):
        """Returns page widget for default application panel."""
        box_page_2 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        label_page_2 = Gtk.Label.new(str='Página 2')
        label_page_2.set_halign(align=Gtk.Align.CENTER)
        label_page_2.set_valign(align=Gtk.Align.CENTER)
        label_page_2.set_hexpand(expand=True)
        label_page_2.set_vexpand(expand=True)
        box_page_2.append(child=label_page_2)

        return box_page_2
