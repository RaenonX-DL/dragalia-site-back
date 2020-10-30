"""Request response body classes."""
from .basic import Response, ResponseKey
from .error import Error400Response, Error404Response, Error405Response, Error422Response, Error500Response
from .post_analysis import (
    CharaAnalysisPublishSuccessResponse, CharaAnalysisPublishFailedResponse,
    CharaAnalysisPublishSuccessResponseKey,
    DragonAnalysisPublishSuccessResponse, DragonAnalysisPublishFailedResponse,
    DragonAnalysisPublishSuccessResponseKey,
    AnalysisPostListResponse, AnalysisPostListResponseKey,
    AnalysisPostGetSuccessResponse, AnalysisPostGetFailedResponse, AnalysisPostGetSuccessResponseKey,
    AnalysisPostEditSuccessResponse, AnalysisPostEditFailedResponse, AnalysisPostEditSuccessResponseKey,
    AnalysisPostIDCheckResponseKey, AnalysisPostIDCheckResponse
)
from .post_quest import (
    QuestPostListResponse, QuestPostListResponseKey,
    QuestPostPublishSuccessResponse, QuestPostPublishFailedResponse,
    QuestPostGetSuccessResponse, QuestPostGetFailedResponse,
    QuestPostEditSuccessResponse, QuestPostEditFailedResponse,
    QuestPostIDCheckResponse
)
from .root import RootTestResponse
from .user import UserLoginResponse
