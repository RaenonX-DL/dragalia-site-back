"""Request response body classes."""
from .basic import Response, ResponseKey
from .post_quest import (
    QuestPostListResponse, QuestPostListResponseKey,
    QuestPostPublishSuccessResponse, QuestPostPublishFailedResponse,
    QuestPostGetSuccessResponse, QuestPostGetFailedResponse,
    QuestPostEditSuccessResponse, QuestPostEditFailedResponse
)
from .user import UserLoginResponse
