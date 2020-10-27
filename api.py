"""Functions for API preparation."""
from flask_restful import Api

from endpoints import (
    EPRootTest, EPUserLogin,
    EPQuestPostList, EPQuestPostGet, EPQuestPostPublish, EPQuestPostEdit, EPQuestPostIDCheck
)
from responses import Error500Response

__all__ = ("attach_api",)


class CustomApi(Api):
    """Customized api wrapped Flask app to enforce the error returned to be the conventionalized format."""

    def handle_error(self, e: Exception):
        """Force the error to be sent in the conventionalized json format."""
        return Error500Response(f"{e.__class__.__name__}: {e}").serialize(), 500


def attach_api(app):
    """Attach api to Flask application."""
    api = CustomApi(app)

    attach_endpoints(api)


def attach_endpoints(api_app):
    """Attach API endpoints to Flask app."""
    api_app.add_resource(EPRootTest, "/", endpoint="misc.root")
    api_app.add_resource(EPUserLogin, "/user/login", endpoint="user.login")
    api_app.add_resource(EPQuestPostList, "/posts/quest", endpoint="posts.quest.list")
    api_app.add_resource(EPQuestPostGet, "/posts/quest/get", endpoint="posts.quest.get")
    api_app.add_resource(EPQuestPostPublish, "/posts/quest/publish", endpoint="posts.quest.publish")
    api_app.add_resource(EPQuestPostEdit, "/posts/quest/edit", endpoint="posts.quest.edit")
    api_app.add_resource(EPQuestPostIDCheck, "/posts/quest/id-check", endpoint="posts.quest.id_check")
