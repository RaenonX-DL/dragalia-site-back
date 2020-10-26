"""Functions for API preparation."""
from flask_restful import Api

from endpoints import EPUserLogin, EPQuestPostList, EPQuestPostGet, EPQuestPostPublish

__all__ = ("attach_endpoints",)


def attach_endpoints(app):
    api = Api(app)
    api.add_resource(EPUserLogin, "/user/login", endpoint="user.login")
    api.add_resource(EPQuestPostList, "/posts/quest", endpoint="posts.quest.list")
    api.add_resource(EPQuestPostGet, "/posts/quest/get", endpoint="posts.quest.get")
    api.add_resource(EPQuestPostPublish, "/posts/quest/publish", endpoint="posts.quest.publish")
