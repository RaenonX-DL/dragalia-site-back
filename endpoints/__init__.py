"""Endpoint resources of the API."""
from .post_analysis import (
    EPAnalysisPostGet, EPAnalysisPostIDCheck, EPAnalysisPostList, EPCharaAnalysisPostEdit,
    EPCharacterAnalysisPostPublish, EPDragonAnalysisPostEdit, EPDragonAnalysisPostPublish,
)
from .post_quest import EPQuestPostEdit, EPQuestPostGet, EPQuestPostIDCheck, EPQuestPostList, EPQuestPostPublish
from .root import EPRootTest
from .user import EPUserLogin, EPUserLoginParam, EPUserShowAds, EPUserShowAdsParam
