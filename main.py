"""Main application."""
from flask import Flask
from flask_cors import CORS

from responses import ResponseBodyEncoder
from api import attach_api
from error import setup_error

__all__ = ("app",)


class AppConfig:
    """Flask app configs."""

    RESTFUL_JSON = {
        "cls": ResponseBodyEncoder
    }


# Initialize app
app = Flask(__name__)
app.config.from_object(AppConfig)

# Setup CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Setup API resources
attach_api(app)

# Setup error handlers
setup_error(app)

# pylint: disable=fixme
# TODO: Setup sleep preventer
# TODO: Google Analytics
# TODO: API Endpoints documentation
# pylint: enable=fixme

if __name__ == "__main__":
    app.run(threaded=True)
