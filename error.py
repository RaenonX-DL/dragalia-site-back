"""Error handlers of the app."""

from responses import Error400Response, Error404Response, Error405Response, Error422Response, Error500Response


def setup_error(app):
    @app.errorhandler(400)
    def handle_400(e):
        return Error400Response(e).serialize()

    @app.errorhandler(404)
    def handle_404(e):
        return Error404Response(e, "Resource not found").serialize()

    @app.errorhandler(405)
    def handle_405(e):
        return Error405Response(e).serialize()

    @app.errorhandler(422)
    def handle_422(e):
        return Error422Response(e).serialize()

    @app.errorhandler(500)
    def handle_500(e):
        return Error500Response(e, "Server error").serialize()
