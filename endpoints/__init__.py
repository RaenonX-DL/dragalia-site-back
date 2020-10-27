"""Endpoint resources of the API."""
from .post_quest import (
    EPQuestPostList, EPQuestPostListParam,
    EPQuestPostPublish, EPQuestPostPublishParam,
    EPQuestPostGet, EPQuestPostGetParam,
    EPQuestPostEdit,
    EPQuestPostIDCheck
)
from .user import EPUserLogin, EPUserLoginParam
