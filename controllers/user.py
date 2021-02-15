"""Google user data controller."""
from datetime import datetime
from enum import Enum
from typing import Optional

from controllers.base import BaseCollection

__all__ = ("GoogleLoginType", "GoogleUserDataKeys", "GoogleUserDataController")


DB_NAME = "user"


class GoogleLoginType(Enum):
    """Google Login outcome."""

    UNKNOWN = -1

    NEW_REGISTER = 0
    ALREADY_REGISTERED = 1


class GoogleUserDataKeys:
    """Keys for a single google user data."""

    GOOGLE_UID = "uid"
    GOOGLE_EMAIL = "em"
    LOGIN_COUNT = "lc"
    LOGIN_RECENT = "lr"
    IS_SITE_ADMIN = "a"
    SHOW_ADS = "ad"


class _GoogleUserDataController(BaseCollection):
    """Google user data controller."""

    database_name = DB_NAME
    collection_name = "google"

    def build_indexes(self):
        self.create_index(GoogleUserDataKeys.GOOGLE_UID, unique=True)

    def user_logged_in(self, uid: str, email: str) -> GoogleLoginType:
        """
        User logged in. If the user data does not exist, create one with ``admin`` set to ``False``.

        :param uid: Google UID of the logged in user
        :param email: Google email of the logged in user
        :return: if the data is updated
        """
        update_result = self.update_one(
            {GoogleUserDataKeys.GOOGLE_UID: uid},
            {
                "$set": {
                    GoogleUserDataKeys.GOOGLE_EMAIL: email,
                    GoogleUserDataKeys.LOGIN_RECENT: datetime.utcnow()
                },
                "$inc": {
                    GoogleUserDataKeys.LOGIN_COUNT: 1
                },
                "$setOnInsert": {
                    GoogleUserDataKeys.IS_SITE_ADMIN: False,
                }
            },
            upsert=True
        )

        if update_result.modified_count > 0:
            return GoogleLoginType.ALREADY_REGISTERED

        if update_result.upserted_id:
            return GoogleLoginType.NEW_REGISTER

        return GoogleLoginType.UNKNOWN

    def get_user_data(self, uid: Optional[str]) -> Optional[dict[str, str]]:
        """
        Get the user data.

        Returns ``None`` if the user data does not exist or ``uid`` is ``None``.

        :param uid: Google UID to get the user data
        :return: user data if found, `None` otherwise
        """
        if not uid:
            return None

        # Prevent number being accidentally passed in
        user_data = self.find_one({GoogleUserDataKeys.GOOGLE_UID: str(uid)})

        return user_data

    def is_user_admin(self, uid: Optional[str]) -> bool:
        """
        Check if the user is a site admin.

        Returns ``False`` if ``uid`` is ``None``.

        :param uid: Google UID of the user to check
        :return: if the user is a site admin
        """
        if not uid:
            return False

        # Prevent number being accidentally passed in
        user_data = self.find_one({GoogleUserDataKeys.GOOGLE_UID: str(uid)})

        return user_data and user_data.get(GoogleUserDataKeys.IS_SITE_ADMIN)


GoogleUserDataController = _GoogleUserDataController()
