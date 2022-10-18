"""Controller for the default apps panel."""

class DefaultApplicationsController:
    """Controller for the default apps panel."""
    def __init__(self):
        self.labels = {
            "x-scheme-handler/http":
                ["Web", ["text/html", "application/xhtml+xml", "x-scheme-handler/https"]],
            "x-scheme-handler/mailto": ["Mail", []],
            "text/calendar": ["Calendar", []],
            "audio/x-vorbis+ogg": ["Music", ["audio/"]],
            "video/x-ogm+ogg": ["Videos", ["video/"]],
            "image/jpeg": ["Photos", ["image/"]],
        }

    def on_app_chooser_changed(self, widget):
        """
        Callback for when app chooser is changed.
        Changes to the choosen app for the main mime type.
        Also changes to the choosen app for the secondary mime types, if supported by the app.
        """
        info = widget.get_app_info()
        mime_type = widget.get_content_type()

        info.set_as_default_for_type(mime_type)

        for extra_types in self.labels[mime_type][1]:
            for supported_type in info.get_supported_types():
                if supported_type.startswith(extra_types):
                    info.set_as_default_for_type(supported_type)
