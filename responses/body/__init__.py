"""Request response body classes."""
from .basic import Response, ResponseKey
from .error import Error400Response, Error404Response, Error405Response, Error422Response, Error500Response
from .post_analysis import (
    AnalysisPostEditFailedResponse, AnalysisPostEditSuccessResponse, AnalysisPostEditSuccessResponseKey,
    AnalysisPostGetFailedResponse, AnalysisPostGetSuccessResponse, AnalysisPostGetSuccessResponseKey,
    AnalysisPostIDCheckResponse, AnalysisPostIDCheckResponseKey, AnalysisPostListResponse, AnalysisPostListResponseKey,
    CharaAnalysisPublishFailedResponse, CharaAnalysisPublishSuccessResponse, CharaAnalysisPublishSuccessResponseKey,
    DragonAnalysisPublishFailedResponse, DragonAnalysisPublishSuccessResponse, DragonAnalysisPublishSuccessResponseKey,
)
from .post_quest import (
    QuestPostEditFailedResponse, QuestPostEditSuccessResponse, QuestPostGetFailedResponse, QuestPostGetSuccessResponse,
    QuestPostIDCheckResponse, QuestPostListResponse, QuestPostListResponseKey, QuestPostPublishFailedResponse,
    QuestPostPublishSuccessResponse,
)
from .root import RootTestResponse
from .user import UserLoginResponse, UserShowAdsResponse
