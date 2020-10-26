"""Endpoints for the user data control."""
from webargs import fields
from webargs.flaskparser import use_args

from controllers import GoogleUserDataController, GoogleLoginType
from responses import UserLoginResponse, ResponseCodeCollection

from .base import EndpointBase, EPParamBase

__all__ = ("EPUserLogin", "EPUserLoginParam")


class EPUserLoginParam(EPParamBase):
    """Parameters for the request of user login."""

    GOOGLE_EMAIL = "google_email"


user_login_args = EndpointBase.base_args() | {
    EPUserLoginParam.GOOGLE_EMAIL: fields.Str()
}


class EPUserLogin(EndpointBase):
    @use_args(user_login_args)
    def post(self, args):
        result = GoogleUserDataController.user_logged_in(args[EPUserLoginParam.GOOGLE_UID],
                                                         args[EPUserLoginParam.GOOGLE_EMAIL])
        if result == GoogleLoginType.UNKNOWN:
            return UserLoginResponse(ResponseCodeCollection.FAILED_LOGIN_NOT_RECORDED), 400

        if result == GoogleLoginType.NEW_REGISTER:
            return UserLoginResponse(ResponseCodeCollection.SUCCESS_NEW), 200

        return UserLoginResponse(ResponseCodeCollection.SUCCESS), 200
