"""Endpoint resources of the API."""
from .post_analysis import (
    EPCharacterAnalysisPostPublish, EPDragonAnalysisPostPublish,
    EPAnalysisPostList,
    EPAnalysisPostGet,
    EPCharaAnalysisPostEdit, EPDragonAnalysisPostEdit,
    EPAnalysisPostIDCheck
)
from .post_quest import EPQuestPostList, EPQuestPostPublish, EPQuestPostGet, EPQuestPostEdit, EPQuestPostIDCheck
from .root import EPRootTest
from .user import EPUserLogin, EPUserLoginParam
