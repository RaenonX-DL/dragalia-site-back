from flask import Flask
from flask_cors import CORS

from responses import ResponseBodyEncoder
from api import attach_endpoints

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
attach_endpoints(app)

# TODO: Setup sleep preventer
# TODO: Google Analytics

if __name__ == "__main__":
    app.run(debug=True)
