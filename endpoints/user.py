"""Endpoints for the user data control."""
from webargs import fields
from webargs.flaskparser import use_args

from controllers import GoogleLoginType, GoogleUserDataController
from responses import ResponseCodeCollection, UserLoginResponse, UserShowAdsResponse
from .base import EPParamBase, EndpointBase

__all__ = ("EPUserLogin", "EPUserLoginParam", "EPUserShowAds", "EPUserShowAdsParam")


# region User Login
class EPUserLoginParam(EPParamBase):
    """Parameters for the request of user login."""

    GOOGLE_EMAIL = "google_email"


user_login_args = EPParamBase.base_args() | {
    EPUserLoginParam.GOOGLE_EMAIL: fields.Str()
}


class EPUserLogin(EndpointBase):
    """Endpoint to send a user login request."""

    @use_args(user_login_args)
    def post(self, args):  # pylint: disable=no-self-use, missing-function-docstring
        result = GoogleUserDataController.user_logged_in(args[EPUserLoginParam.GOOGLE_UID],
                                                         args[EPUserLoginParam.GOOGLE_EMAIL])
        if result == GoogleLoginType.UNKNOWN:
            return UserLoginResponse(ResponseCodeCollection.FAILED_LOGIN_NOT_RECORDED), 400

        if result == GoogleLoginType.NEW_REGISTER:
            return UserLoginResponse(ResponseCodeCollection.SUCCESS_NEW), 200

        return UserLoginResponse(ResponseCodeCollection.SUCCESS), 200


# endregion


# region User Show Ads
class EPUserShowAdsParam(EPParamBase):
    """Parameters for the request of checking if the ads for an user shoulw be shown."""


user_show_ads_args = EPParamBase.base_args()


class EPUserShowAds(EndpointBase):
    """Endpoint to send a user ads disable check request."""

    @use_args(user_show_ads_args, location="query")
    def get(self, args):  # pylint: disable=no-self-use, missing-function-docstring
        show_ads = GoogleUserDataController.is_user_show_ads(args[EPUserLoginParam.GOOGLE_UID])

        return UserShowAdsResponse(show_ads), 200
# endregion
