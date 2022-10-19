"""Controller for the default apps panel."""

from .model import Model

class Controller:
    """Controller for the default apps panel."""
    def __init__(self, model=Model()):
        self.model = model

    def set_default_app(self, app_info, mimetype):
        """
        Sets the default application of @mimetype to @app_info.
        Also, sets @app_info as the default application for allsecondary mimetypes,
        if supported by @app_info.
        """
        app_info.set_as_default_for_type(mimetype)

        for extra_types in self.model.labels[mimetype][1]:
            for supported_type in app_info.get_supported_types():
                if supported_type.startswith(extra_types):
                    app_info.set_as_default_for_type(supported_type)
