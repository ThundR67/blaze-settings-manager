"""Panel to customize mouse and touchpad settings."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

from . import constants
from ..common import preference, config

class MouseAndTouchpad:
    """Panel to customize mouse and touchpad settings."""
    def __init__(self):
        self.config = config.Config(constants.CONFIG_NAME)

        self.name = constants.PANEL_NAME
        self.icon = constants.PANEL_ICON

        self.widget = Adw.Bin.new()

        page = Adw.PreferencesPage.new()

        #page.add(self.get_general_group())
        page.add(self.get_mouse_group())
        page.add(self.get_touchpad_group())

        self.widget.set_child(page)



    def get_mouse_group(self):
        """Return the mouse group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Mouse")

        # Mouse speed slider.
        mouse_speed_selector = preference.Preference(
            preference.PreferenceType.SLIDER,
            "Mouse speed",
            constants.MOUSE_SPPEED_PATH,
            self.config,
        )

        # Natural scrolling switch.
        natural_scrolling_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Natural scrolling",
            constants.MOUSE_NATURAL_SCROLLING_PATH,
            self.config,
        )

        group.add(mouse_speed_selector.get_widget())
        group.add(natural_scrolling_selector.get_widget())

        return group

    def get_touchpad_group(self):
        """Return the touchpad group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Touchpad")

        # Touchpad enabled switch.
        touchpad_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Enable touchpad",
            constants.TOUCHPAD_ENABLED_PATH,
            self.config,
        )

        # Touchpad speed slider.
        touchpad_speed_selector = preference.Preference(
            preference.PreferenceType.SLIDER,
            "Touchpad speed",
            constants.TOUCHPAD_SPEED_PATH,
            self.config,
        )

        # Natural scrolling switch.
        natural_scrolling_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Natural scrolling",
            constants.TOUCHPAD_NATURAL_SCROLLING_PATH,
            self.config,
        )

        # Tap to click switch.
        tap_to_click_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Tap to click",
            constants.TOUCHPAD_TAP_TO_CLICK_PATH,
            self.config,
        )

        # Two finger scrolling switch.
        two_finger_scrolling_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Two finger scrolling",
            constants.TOUCHPAD_TWO_FINGER_SCROLLING_PATH,
            self.config,
        )

        # Edge scrolling switch.
        edge_scrolling_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Edge scrolling",
            constants.TOUCHPAD_EDGE_SCROLLING_PATH,
            self.config,
        )

        group.add(touchpad_selector.get_widget())
        group.add(touchpad_speed_selector.get_widget())
        group.add(natural_scrolling_selector.get_widget())
        group.add(tap_to_click_selector.get_widget())
        group.add(two_finger_scrolling_selector.get_widget())
        group.add(edge_scrolling_selector.get_widget())

        return group


"""
    def get_general_group(self):
        group = Adw.PreferencesGroup.new()
        group.set_title("General")

        # Primary button selector.
        primary_button_combo_row = Adw.ComboRow.new()
        primary_button_combo_row.set_title("Primary button")
        primary_button_combo_row.set_subtitle(
            "Sets the order of physical button on mice and touchpads.")

        primary_button_model = Gtk.StringList.new([
            i.capitalize() for i in self.controller.primary_buttons]
        )

        primary_button_combo_row.set_model(primary_button_model)

        current_primary_button = self.controller.get_primary_button()
        primary_button_combo_row.set_selected(
            self.controller.primary_buttons.index(current_primary_button))

        primary_button_combo_row.connect("notify::selected", self.on_primary_button_combo_row_selected)

        group.add(primary_button_combo_row)

        return group

    def on_primary_button_combo_row_selected(self, widget, _):
        selected = widget.get_selected_item().get_string().lower()
        self.controller.set_primary_button(selected)
"""