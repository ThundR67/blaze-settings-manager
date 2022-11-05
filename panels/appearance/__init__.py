"""Panel to customize colorscheme and wallpaper."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gdk, Gtk

from ..common import preference, config
from . import constants


def _get_screen_size():
    """Return the screen size."""
    display = Gdk.Display.get_default()
    mon_geoms = [
        screen.get_geometry()
        for screen in display.get_monitors()
    ]

    x_0 = min(r.x            for r in mon_geoms)
    y_0 = min(r.y            for r in mon_geoms)
    x_1 = max(r.x + r.width  for r in mon_geoms)
    y_1 = max(r.y + r.height for r in mon_geoms)

    return x_1 - x_0, y_1 - y_0

(_WIDTH, _HEIGHT) = _get_screen_size()

class AppearanceView:
    """Panel to customize colorscheme and wallpaper."""
    def __init__(self, parent):
        self.config = config.Config(constants.CONFIG_NAME)
        self.parent = parent

        self.name = constants.PANEL_NAME
        self.icon = constants.PANEL_ICON

        self.widget = Adw.Bin.new()

        page = Adw.PreferencesPage.new()

        page.add(self.get_colorscheme_group())
        page.add(self.get_wallpaper_group())

        self.widget.set_child(page)

    def get_colorscheme_group(self):
        """Returns colorscheme group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Style")

        # Colorscheme selector.
        colorscheme_selector = preference.Preference(
            preference.PreferenceType.DROPDOWN,
            "Colorscheme",
            constants.COLORSCHEME_PATH,
            self.config,
            values=["dracula", "gruvbox", "nord"],
        )

        group.add(colorscheme_selector.get_widget())

        return group

    def get_wallpaper_group(self):
        """Returns wallpaper group."""


        group = Adw.PreferencesGroup.new()
        group.set_title("Wallpaper")


        row = Adw.ActionRow.new()
        row.set_title("Wallpaper")

        clamp = Adw.Clamp.new()
        clamp.set_css_classes(["card"])

        self.column = Gtk.FlowBox.new()
        self.column.set_css_classes(["box"])
        self.column.set_selection_mode(Gtk.SelectionMode.NONE)
        self.column.set_column_spacing(12)
        self.column.set_min_children_per_line(3)
        self.column.set_max_children_per_line(3)
        self.column.set_homogeneous(True)
        self.column.set_activate_on_single_click(True)

        self.column.set_margin_top(12)
        self.column.set_margin_bottom(12)
        self.column.set_margin_start(12)
        self.column.set_margin_end(12)

        button = Gtk.Button.new_with_label("Add Picture")
        button.set_css_classes(["flat", "image-text-button"])

        button_content = Adw.ButtonContent.new()
        button_content.set_icon_name("list-add-symbolic")
        button_content.set_label("Add Picture")

        button.set_child(button_content)
        button.connect("clicked", self.on_add_picture_clicked, self.column)

        group.set_header_suffix(button)

        for location in self.config.get(constants.WALLPAPER_LOCATIONS_PATH):
            self.add_wallpaper(location)

        clamp.set_child(self.column)
        group.add(clamp)

        return group

    def add_wallpaper(self, location):
        """Adds a wallpaper to the wallpaper list in wallpaper group."""

        picture = Gtk.Picture.new_for_filename(location)
        picture.set_size_request(_HEIGHT*0.01, _WIDTH*0.01)
        picture.set_halign(Gtk.Align.START)

        picture.set_css_classes(["card"])
        picture.set_content_fit(Gtk.ContentFit.FILL)

        overlay = Gtk.Overlay.new()
        close_button = Gtk.Button.new_from_icon_name("window-close-symbolic")

        close_button.set_css_classes([
            "osd",
            "image-button",
            "remove-button",
            "top",
            "right",
            "circular"
        ])

        close_button.set_margin_top(6)
        close_button.set_margin_end(6)
        close_button.set_valign(Gtk.Align.START)
        close_button.set_halign(Gtk.Align.END)

        close_button.connect("clicked", self.on_remove_picture_clicked, location)

        overlay.add_overlay(close_button)

        overlay.set_child(picture)

        self.column.append(overlay)

    def remove_wallpaper(self, location):
        """Removes a wallpaper from the wallpaper list in wallpaper group."""
        locations = self.config.get(constants.WALLPAPER_LOCATIONS_PATH)
        index = locations.index(location)
        child = self.column.get_child_at_index(index)
        self.column.remove(child)

    def on_remove_picture_clicked(self, button, location):
        """Removes a wallpaper from the wallpaper list in wallpaper group."""
        self.remove_wallpaper(location)
        locations = self.config.get(constants.WALLPAPER_LOCATIONS_PATH)
        locations.remove(location)
        self.config.set(constants.WALLPAPER_LOCATIONS_PATH, locations)
        self.config.save()

    def on_add_picture_clicked(self, _, column):
        """Lets user pick an image file."""
        dialog = Gtk.FileChooserDialog(
            title="Choose a picture",
            parent=self.parent,
            action=Gtk.FileChooserAction.OPEN,
        )

        dialog.set_select_multiple(True)
        dialog.set_transient_for(self.parent)

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)


        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Open", Gtk.ResponseType.OK)


        dialog.connect("response", self.on_add_picture_response, column)

        dialog.show()


    def on_add_picture_response(self, dialog, response, column):
        """Adds picture to the wallpaper list."""
        location = self.config.get(constants.WALLPAPER_LOCATIONS_PATH)

        if response == Gtk.ResponseType.OK:
            for file in dialog.get_files():
                if file.get_path() not in location:
                    location.append(file.get_path())
                    self.add_wallpaper(file.get_path())

            self.config.set(constants.WALLPAPER_LOCATIONS_PATH, location)
            self.config.save()


        dialog.destroy()
