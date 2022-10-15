"""Panel to customize mouse and touchpad settings."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

_PRIMARY_BUTTON_CONFIG = "desktop.general.primary_button"

_MOUSE_SPPEED_CONFIG = "desktop.mouse.speed"
_MOUSE_NATURAL_SCROLLING_CONFIG = "desktop.mouse.natural_scrolling"

_TOUCHPAD_ENABLED_CONFIG = "desktop.touchpad.enabled"
_TOUCHPAD_EDGE_SCROLLING_CONFIG = "desktop.touchpad.edge_scrolling"
_TOUCHPAD_NATURAL_SCROLLING_CONFIG = "desktop.touchpad.natural_scrolling"
_TOUCHPAD_TAP_TO_CLICK_CONFIG = "desktop.touchpad.tap_to_click"
_TOUCHPAD_SPEED_CONFIG = "desktop.touchpad.speed"
_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG = "desktop.touchpad.two_finger_scrolling"

_PRIMARY_BUTTONS = ["left", "right"]

class MouseAndTouchpad:
    def __init__(self, config):
        self.config = config

        self.name = "Mouse and Touchpad"
        self.icon = "org.gnome.Settings-mouse-symbolic"

        self.widget = Adw.Bin.new()

        preferences_page = Adw.PreferencesPage.new()


        preferences_page.add(self.get_general_group())
        preferences_page.add(self.get_mouse_group())
        preferences_page.add(self.get_touchpad_group())

        self.widget.set_child(preferences_page)

    def get_general_group(self):
        """Return the general group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("General")

        # Primary button selector.
        primary_button_combo_row = Adw.ComboRow.new()
        primary_button_combo_row.set_title("Primary button")
        primary_button_combo_row.set_subtitle(
            "Sets the order of physical button on mice and touchpads."
        )

        primary_button_model = Gtk.StringList.new([
            i.capitalize() for i in _PRIMARY_BUTTONS]
        )

        primary_button_combo_row.set_model(primary_button_model)

        current_primary_button = self.config.get(_PRIMARY_BUTTON_CONFIG)
        primary_button_combo_row.set_selected(_PRIMARY_BUTTONS.index(current_primary_button))

        primary_button_combo_row.connect("notify::selected", self.on_primary_button_combo_row_selected)

        group.add(primary_button_combo_row)

        return group

    def on_primary_button_combo_row_selected(self, widget, _):
        """Handle primary button selection."""
        selected = widget.get_selected_item().get_string().lower()
        self.config.set(_PRIMARY_BUTTON_CONFIG, selected)
        self.config.save()

    def get_mouse_group(self):
        """Return the mouse group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Mouse")

        # Mouse speed slider.
        mouse_speed_row = Adw.ActionRow.new()
        mouse_speed_row.set_title("Mouse speed")


        mouse_speed_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        mouse_speed_scale.set_hexpand(True)
        mouse_speed_scale.set_vexpand(True)

        mouse_speed_scale.set_value(self.config.get(_MOUSE_SPPEED_CONFIG))
        mouse_speed_scale.connect("value-changed", self.on_mouse_speed_scale_value_changed)

        mouse_speed_row.add_suffix(mouse_speed_scale)

        # Natural scrolling switch.
        natural_scrolling_row = Adw.ActionRow.new()
        natural_scrolling_row.set_title("Natural scrolling")
        natural_scrolling_row.set_subtitle("Scrolling moves the content, not the view.")


        natural_scrolling_switch = Gtk.Switch.new()
        natural_scrolling_switch.set_valign(Gtk.Align.CENTER)

        natural_scrolling_switch.set_active(self.config.get(_MOUSE_NATURAL_SCROLLING_CONFIG))
        natural_scrolling_switch.connect("notify::active", self.on_mouse_natural_scrolling_switch_active)

        natural_scrolling_row.add_suffix(natural_scrolling_switch)

        group.add(mouse_speed_row)
        group.add(natural_scrolling_row)

        return group

    def on_mouse_speed_scale_value_changed(self, widget):
        """Handle mouse speed change."""
        self.config.set(_MOUSE_SPPEED_CONFIG, int(widget.get_value()))
        self.config.save()

    def on_mouse_natural_scrolling_switch_active(self, widget, _):
        """Handle mouse natural scrolling change."""
        self.config.set(_MOUSE_NATURAL_SCROLLING_CONFIG, widget.get_active())
        self.config.save()

    def get_touchpad_group(self):
        """Return the touchpad group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Touchpad")

        # Touchpad enabled switch.
        touchpad_enabled_row = Adw.ActionRow.new()
        touchpad_enabled_row.set_title("Touchpad")


        touchpad_enabled_switch = Gtk.Switch.new()
        touchpad_enabled_switch.set_valign(Gtk.Align.CENTER)

        touchpad_enabled_switch.set_active(self.config.get(_TOUCHPAD_ENABLED_CONFIG))
        touchpad_enabled_switch.connect("notify::active", self.on_touchpad_enabled_switch_active)

        touchpad_enabled_row.add_suffix(touchpad_enabled_switch)

        # Touchpad speed slider.
        touchpad_speed_row = Adw.ActionRow.new()
        touchpad_speed_row.set_title("Mouse speed")


        touchpad_speed_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        touchpad_speed_scale.set_hexpand(True)
        touchpad_speed_scale.set_vexpand(True)

        touchpad_speed_scale.set_value(self.config.get(_TOUCHPAD_SPEED_CONFIG))
        touchpad_speed_scale.connect("value-changed", self.on_touchpad_speed_scale_value_changed)

        touchpad_speed_row.add_suffix(touchpad_speed_scale)

        # Natural scrolling switch.
        natural_scrolling_row = Adw.ActionRow.new()
        natural_scrolling_row.set_title("Natural scrolling")
        natural_scrolling_row.set_subtitle("Scrolling moves the content, not the view.")

        natural_scrolling_switch = Gtk.Switch.new()
        natural_scrolling_switch.set_valign(Gtk.Align.CENTER)

        natural_scrolling_switch.set_active(self.config.get(_TOUCHPAD_NATURAL_SCROLLING_CONFIG))
        natural_scrolling_switch.connect("notify::active", self.on_touchpad_natural_scrolling_switch_active)

        natural_scrolling_row.add_suffix(natural_scrolling_switch)

        # Tap to click switch.
        tap_to_click_row = Adw.ActionRow.new()
        tap_to_click_row.set_title("Tap to click")

        tap_to_click_switch = Gtk.Switch.new()
        tap_to_click_switch.set_valign(Gtk.Align.CENTER)

        tap_to_click_switch.set_active(self.config.get(_TOUCHPAD_TAP_TO_CLICK_CONFIG))
        tap_to_click_switch.connect("notify::active", self.on_touchpad_tap_to_click_switch_active)

        tap_to_click_row.add_suffix(tap_to_click_switch)

        # Two finger scrolling switch.
        two_finger_scrolling_row = Adw.ActionRow.new()
        two_finger_scrolling_row.set_title("Two finger scrolling")

        two_finger_scrolling_switch = Gtk.Switch.new()
        two_finger_scrolling_switch.set_valign(Gtk.Align.CENTER)

        two_finger_scrolling_switch.set_active(self.config.get(_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG))
        two_finger_scrolling_switch.connect("notify::active", self.on_touchpad_two_finger_scrolling_switch_active)

        two_finger_scrolling_row.add_suffix(two_finger_scrolling_switch)

        # Edge scrolling switch.
        edge_scrolling_row = Adw.ActionRow.new()
        edge_scrolling_row.set_title("Edge scrolling")

        edge_scrolling_switch = Gtk.Switch.new()
        edge_scrolling_switch.set_valign(Gtk.Align.CENTER)

        edge_scrolling_switch.set_active(self.config.get(_TOUCHPAD_EDGE_SCROLLING_CONFIG))
        edge_scrolling_switch.connect("notify::active", self.on_touchpad_edge_scrolling_switch_active)

        edge_scrolling_row.add_suffix(edge_scrolling_switch)

        group.add(touchpad_enabled_row)
        group.add(touchpad_speed_row)
        group.add(natural_scrolling_row)
        group.add(tap_to_click_row)
        group.add(two_finger_scrolling_row)
        group.add(edge_scrolling_row)

        return group

    def on_touchpad_enabled_switch_active(self, widget, _):
        """Handle touchpad enabled change."""
        self.config.set(_TOUCHPAD_ENABLED_CONFIG, widget.get_active())
        self.config.save()

    def on_touchpad_speed_scale_value_changed(self, widget):
        """Handle touchpad speed change."""
        self.config.set(_TOUCHPAD_SPEED_CONFIG, int(widget.get_value()))
        self.config.save()

    def on_touchpad_natural_scrolling_switch_active(self, widget, _):
        """Handle touchpad natural scrolling change."""
        self.config.set(_TOUCHPAD_NATURAL_SCROLLING_CONFIG, widget.get_active())
        self.config.save()

    def on_touchpad_tap_to_click_switch_active(self, widget, _):
        """Handle touchpad tap to click change."""
        self.config.set(_TOUCHPAD_TAP_TO_CLICK_CONFIG, widget.get_active())
        self.config.save()

    def on_touchpad_two_finger_scrolling_switch_active(self, widget, _):
        """Handle touchpad two finger scrolling change."""
        self.config.set(_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG, widget.get_active())
        self.config.save()

    def on_touchpad_edge_scrolling_switch_active(self, widget, _):
        """Handle touchpad edge scrolling change."""
        self.config.set(_TOUCHPAD_EDGE_SCROLLING_CONFIG, widget.get_active())
        self.config.save()
