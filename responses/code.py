"""Response code to be attached in EVERY responses."""
from dataclasses import dataclass

__all__ = ("ResponseCode", "ResponseCodeCollection")


@dataclass
class ResponseCode:
    code: int
    success: bool
    description: str


class ResponseCodeCollection:
    """Response code for a request."""

    # Remember to update `doc/response_code` if there's any change

    SUCCESS = \
        ResponseCode(100, True, "Request succeed.")
    SUCCESS_NEW = \
        ResponseCode(101, True, "Request succeed with some data newly registered.")
    SUCCESS_NO_CHANGE = \
        ResponseCode(102, True, "Request succeed with nothing changed.")

    FAILED_LOGIN_NOT_RECORDED = \
        ResponseCode(200, False, "Failed to record the login of a user.")
    FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN = \
        ResponseCode(201, False, "Failed to publish the quest post. User is not a site admin.")
    FAILED_POST_NOT_EXISTS = \
        ResponseCode(202, False, "Post not exists.")
    FAILED_CHECK_NOT_ADMIN = \
        ResponseCode(203, False, "Check failed because the user is not an admin.")

    FAILED_SERVER_ERROR = \
        ResponseCode(901, False, "Request failed with server side error.")
    FAILED_UNKNOWN = \
        ResponseCode(999, False, "Request failed with unknown reason.")
