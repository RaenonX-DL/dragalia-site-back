"""Endpoints to get the data related to quest posts."""
from webargs import fields
from webargs.flaskparser import use_args

from controllers import GoogleUserDataController, QuestPostController, QuestPostKey
from responses import (
    ResponseCodeCollection,
    QuestPostListResponse,
    QuestPostPublishSuccessResponse, QuestPostPublishFailedResponse,
    QuestPostGetSuccessResponse, QuestPostGetFailedResponse
)

from .base import EndpointBase, EPParamBase

__all__ = ("EPQuestPostPublish", "EPQuestPostPublishParam",
           "EPQuestPostList", "EPQuestPostListParam",
           "EPQuestPostGet", "EPQuestPostGetParam")


class EPQuestPostPublishParam(EPParamBase):
    """Parameters for the request of publishing a quest post."""

    TITLE = "title"
    LANG_CODE = "lang"
    GENERAL_INFO = "general"
    VIDEO = "video"
    POSITION_INFO = "positional"
    ADDENDUM = "addendum"

    # Subfield of `POSITIONAL_INFO`

    POS_INFO_POSITION = "position"
    POS_INFO_BUILDS = "builds"
    POS_INFO_ROTATIONS = "rotations"
    POS_INFO_TIPS = "tips"

    @classmethod
    def pos_info_to_model_key(cls, position_info: list[dict[str, str]]) -> list[dict[str, str]]:
        """
        Change the positional info to use model key.

        :param position_info: positional info to replace the key
        :return: positional info using model key
        """
        ret = []

        for pos_info in position_info:
            ret.append({
                QuestPostKey.INFO_POSITION: pos_info[cls.POS_INFO_POSITION],
                QuestPostKey.INFO_BUILDS: pos_info[cls.POS_INFO_BUILDS],
                QuestPostKey.INFO_ROTATIONS: pos_info[cls.POS_INFO_ROTATIONS],
                QuestPostKey.INFO_TIPS: pos_info[cls.POS_INFO_TIPS]
            })

        return ret


quest_post_pub_args = EndpointBase.base_args() | {
    EPQuestPostPublishParam.TITLE: fields.Str(),
    EPQuestPostPublishParam.LANG_CODE: fields.Str(),
    EPQuestPostPublishParam.GENERAL_INFO: fields.Str(),
    EPQuestPostPublishParam.VIDEO: fields.Str(),
    EPQuestPostPublishParam.POSITION_INFO: fields.List(fields.Dict(keys=fields.Str(), values=fields.Str())),
    EPQuestPostPublishParam.ADDENDUM: fields.Str(),
}


class EPQuestPostPublish(EndpointBase):
    """Endpoint resource to publish a post."""

    @use_args(quest_post_pub_args)
    def post(self, args):
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostPublishParam.GOOGLE_UID])
        if not is_user_admin:
            return QuestPostPublishFailedResponse(ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        title = args[EPQuestPostPublishParam.TITLE]
        lang_code = args[EPQuestPostPublishParam.LANG_CODE]
        general_info = args[EPQuestPostPublishParam.GENERAL_INFO]
        video = args[EPQuestPostPublishParam.VIDEO]
        positional_info = EPQuestPostPublishParam.pos_info_to_model_key(args[EPQuestPostPublishParam.POSITION_INFO])
        addendum = args[EPQuestPostPublishParam.ADDENDUM]

        new_seq_id = QuestPostController.publish_post(title, lang_code, general_info, video, positional_info, addendum)

        return QuestPostPublishSuccessResponse(new_seq_id), 200


class EPQuestPostListParam(EPParamBase):
    """Parameters for the request of a list of quest posts."""

    START = "start"
    LIMIT = "limit"


quest_post_list_args = EndpointBase.base_args() | {
    EPQuestPostListParam.START: fields.Int(default=0),
    EPQuestPostListParam.LIMIT: fields.Int(default=25)
}


class EPQuestPostList(EndpointBase):
    """Endpoint resource to get a quest post list."""

    @use_args(quest_post_list_args, location="query")
    def get(self, args):
        start_idx = args[EPQuestPostListParam.START]

        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostListParam.GOOGLE_UID])
        posts = QuestPostController.get_posts(start=start_idx, limit=args[EPQuestPostListParam.LIMIT])

        return QuestPostListResponse(is_user_admin, posts, start_idx), 200


class EPQuestPostGetParam(EPParamBase):
    """Parameters for the request of getting a quest post."""

    SEQ_ID = "seq_id"
    LANG_CODE = "lang_code"


quest_post_get_args = EndpointBase.base_args() | {
    EPQuestPostGetParam.SEQ_ID: fields.Int(default=0),
    EPQuestPostGetParam.LANG_CODE: fields.Str()
}


class EPQuestPostGet(EndpointBase):
    """Endpoint resource to get a post."""

    @use_args(quest_post_get_args, location="query")
    def get(self, args):
        seq_id = args[EPQuestPostGetParam.SEQ_ID]

        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostGetParam.GOOGLE_UID])
        post = QuestPostController.get_post(seq_id, args[EPQuestPostGetParam.LANG_CODE])

        if not post:
            return QuestPostGetFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 200

        return QuestPostGetSuccessResponse(is_user_admin, post), 200
