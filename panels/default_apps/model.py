"""Model for the default apps panel."""

class Model:
    """Model for the default app panel."""
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
