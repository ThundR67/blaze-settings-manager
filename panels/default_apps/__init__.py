"""Panel to customize default applications."""

class DefaultApplications:
    """Panel to customize default applications."""

    def __init__(self):
        self.name = "Default Applications"
        self.icon = "org.gnome.Settings-default-apps-symbolic"

    def on_default_apps_clicked(self, button):
        """Open the default applications panel."""
        self.window.leaflets[0].set_visible_child_name("default-apps")