"""Error handlers of the app."""

from responses import Error400Response, Error404Response, Error405Response, Error422Response, Error500Response


def setup_error(app):
    """Setup errors for ``app``."""
    # pylint: disable=unused-variable
    @app.errorhandler(400)
    def handle_400(error):
        return Error400Response(error).serialize()

    @app.errorhandler(404)
    def handle_404(error):
        return Error404Response(error, "Resource not found").serialize()

    @app.errorhandler(405)
    def handle_405(error):
        return Error405Response(error).serialize()

    @app.errorhandler(422)
    def handle_422(error):
        return Error422Response(error).serialize()

    @app.errorhandler(500)
    def handle_500(error):
        return Error500Response(error, "Server error").serialize()
