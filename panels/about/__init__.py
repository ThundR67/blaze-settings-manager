"""Panel to display system information"""
from .controller import Controller

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

class AboutView:
    """Panel to display system information"""
    def __init__(self, controller=Controller()):
        self.controller = controller

        self.name = "About"
        self.icon = "org.gnome.Settings-about-symbolic"

        self.widget = Adw.Bin.new()

        preferences_page = Adw.PreferencesPage.new()

        preferences_page.add(self.get_hostname_group())
        preferences_page.add(self.get_hardware_group())
        preferences_page.add(self.get_software_group())

        toast_overlay = Adw.ToastOverlay.new()
        toast_overlay.set_child(preferences_page)

        self.toast = Adw.Toast.new("Invalid hostname")

        self.widget.set_child(toast_overlay)

    def get_hostname_group(self):
        """Return the hostname group."""
        group = Adw.PreferencesGroup.new()

        row = Adw.ActionRow.new()
        row.set_title("Device Name")

        stack = Gtk.Stack.new()

        label = Gtk.Label.new()
        label.set_valign(Gtk.Align.CENTER)
        label.set_css_classes(["dim-label"])
        label.set_halign(Gtk.Align.END)
        label.set_text(self.controller.get_hostname())


        toggle_button = Gtk.ToggleButton.new()
        toggle_button.set_icon_name("document-edit-symbolic")
        toggle_button.set_valign(Gtk.Align.CENTER)

        toggle_button.connect(
            "toggled",
            self.on_hostname_toggle,
            stack,
        )

        entry = Gtk.Entry.new()
        entry.set_valign(Gtk.Align.CENTER)
        entry.set_text(self.controller.get_hostname())
        entry.connect(
            "activate",
            self.on_hostname_entry_activation,
            label,
            stack,
            toggle_button,
        )

        stack.add_named(label, "label")
        stack.add_named(entry, "entry")

        row.add_suffix(stack)
        row.add_suffix(toggle_button)

        group.add(row)

        return group

    def on_hostname_toggle(self, toggle_button, stack):
        """Toggle the edit mode of the hostname."""
        if toggle_button.get_active():
            stack.set_visible_child_name("entry")
            stack.get_visible_child().grab_focus()
            return

        stack.set_visible_child_name("label")
        toggle_button.set_active(False)

    def on_hostname_entry_activation(self, entry, label, stack, toggle_button, toast):
        """Set the hostname when the entry is activated."""
        hostname = entry.get_text()
        if self.controller.set_hostname(hostname):
            toast.dismiss()
            label.set_text(hostname)
            entry.set_text(hostname)
            stack.set_visible_child_name("label")
            toggle_button.set_active(False)
            return


        self.widget.get_child().add_toast(self.toast)

    def get_hardware_group(self):
        """Return the hardware group."""
        hardware_info = self.controller.get_hardware_info()

        rows = {
            "Model": f"{hardware_info.vendor} {hardware_info.product_name}",
            "Processor": hardware_info.processor,
            "Graphics": hardware_info.graphics,
            "Memory": f"{hardware_info.memory:.2f} GB",
            "Disk": f"{hardware_info.disk:.2f} GB",
        }

        group = Adw.PreferencesGroup.new()
        group.set_title("Hardware")

        for key, value in rows.items():
            row = Adw.ActionRow.new()
            row.set_title(key)

            label = Gtk.Label.new(value)
            label.set_valign(Gtk.Align.CENTER)
            label.set_css_classes(["dim-label"])

            row.add_suffix(label)

            group.add(row)

        return group

    def get_software_group(self):
        """Return the software group."""
        software_info = self.controller.get_software_info()

        rows = {
            "OS Name": software_info.os_name,
            "OS Type": software_info.os_type,
            "Kernel": software_info.kernel,
        }

        group = Adw.PreferencesGroup.new()
        group.set_title("Software")

        for key, value in rows.items():
            row = Adw.ActionRow.new()
            row.set_title(key)

            label = Gtk.Label.new(value)
            label.set_valign(Gtk.Align.CENTER)
            label.set_css_classes(["dim-label"])

            row.add_suffix(label)

            group.add(row)

        return group
