"""Response body for user data control."""
from responses.code import ResponseCodeCollection

from .basic import Response, ResponseKey

__all__ = ("UserLoginResponse", "UserShowAdsResponse")


class UserLoginResponse(Response):
    """Response body for user login."""


class UserShowAdsResponseKey(ResponseKey):
    """
    Response keys of checking the ads availability of an user.

    Keys must be consistent with the type ``UserShowAdsResponse`` at the front side.
    """

    SHOW_ADS = "showAds"


class UserShowAdsResponse(Response):
    """Response body of checking the ads availability of an user."""

    def __init__(self, show_ads: bool):
        super().__init__(ResponseCodeCollection.SUCCESS)

        self._show_ads = show_ads

    def serialize(self):
        return super().serialize() | {
            UserShowAdsResponseKey.SHOW_ADS: self._show_ads,
        }
