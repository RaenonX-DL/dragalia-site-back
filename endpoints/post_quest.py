"""Endpoints to get the data related to quest posts."""
from webargs import fields
from webargs.flaskparser import use_args

from controllers import GoogleUserDataController, QuestPostController, QuestPostKey
from controllers.results import UpdateResult
from responses import (
    ResponseCodeCollection,
    QuestPostListResponse,
    QuestPostPublishSuccessResponse, QuestPostPublishFailedResponse,
    QuestPostGetSuccessResponse, QuestPostGetFailedResponse,
    QuestPostEditSuccessResponse, QuestPostEditFailedResponse,
    QuestPostIDCheckResponse
)

from .base import EndpointBase, EPParamBase

__all__ = ("EPQuestPostPublish", "EPQuestPostPublishParam",
           "EPQuestPostList", "EPQuestPostListParam",
           "EPQuestPostGet", "EPQuestPostGetParam",
           "EPQuestPostEdit",
           "EPQuestPostIDCheck")


# region Quest Post / Publish

class EPQuestPostPublishParam(EPParamBase):
    """Parameters for the request of publishing a quest post."""

    SEQ_ID = "seq_id"
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
    EPQuestPostPublishParam.SEQ_ID: fields.Int(),
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

        seq_id = args[EPQuestPostPublishParam.SEQ_ID]
        title = args[EPQuestPostPublishParam.TITLE]
        lang_code = args[EPQuestPostPublishParam.LANG_CODE]
        general_info = args[EPQuestPostPublishParam.GENERAL_INFO]
        video = args[EPQuestPostPublishParam.VIDEO]
        positional_info = EPQuestPostPublishParam.pos_info_to_model_key(args[EPQuestPostPublishParam.POSITION_INFO])
        addendum = args[EPQuestPostPublishParam.ADDENDUM]

        new_seq_id = QuestPostController.publish_post(
            title, lang_code, general_info, video, positional_info, addendum, seq_id=seq_id
        )

        return QuestPostPublishSuccessResponse(new_seq_id), 200


# endregion


# region Quest Post / List

class EPQuestPostListParam(EPParamBase):
    """Parameters for the request of a list of quest posts."""

    LANG_CODE = "lang_code"
    START = "start"
    LIMIT = "limit"


quest_post_list_args = EndpointBase.base_args() | {
    EPQuestPostListParam.LANG_CODE: fields.Str(),
    EPQuestPostListParam.START: fields.Int(default=0),
    EPQuestPostListParam.LIMIT: fields.Int(default=25)
}


class EPQuestPostList(EndpointBase):
    """Endpoint resource to get a quest post list."""

    @use_args(quest_post_list_args, location="query")
    def get(self, args):
        start_idx = args[EPQuestPostListParam.START]

        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostListParam.GOOGLE_UID])
        lang_code = args[EPQuestPostListParam.LANG_CODE]
        posts, post_count = QuestPostController.get_posts(
            lang_code, start=start_idx, limit=args[EPQuestPostListParam.LIMIT]
        )

        return QuestPostListResponse(is_user_admin, posts, start_idx, post_count), 200


# endregion


# region Quest Post / Get

class EPQuestPostGetParam(EPParamBase):
    """Parameters for the request of getting a quest post."""

    SEQ_ID = "seq_id"
    LANG_CODE = "lang"
    INCREASE_COUNT = "inc_count"


quest_post_get_args = EndpointBase.base_args() | {
    EPQuestPostGetParam.SEQ_ID: fields.Int(default=0),
    EPQuestPostGetParam.LANG_CODE: fields.Str(),
    EPQuestPostGetParam.INCREASE_COUNT: fields.Bool()
}


class EPQuestPostGet(EndpointBase):
    """Endpoint resource to get a post."""

    @use_args(quest_post_get_args, location="query")
    def get(self, args):
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostGetParam.GOOGLE_UID])

        seq_id = args[EPQuestPostGetParam.SEQ_ID]
        lang_code = args[EPQuestPostGetParam.LANG_CODE]
        increase_count = args[EPQuestPostGetParam.INCREASE_COUNT]
        result = QuestPostController.get_post(seq_id, lang_code, increase_count)

        if not result.post:
            return QuestPostGetFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 404

        return QuestPostGetSuccessResponse(is_user_admin, result), 200


# endregion


# region Quest Post / Edit

class EPQuestPostEditParam(EPQuestPostPublishParam):
    """Parameters for the request of editting a quest post."""

    SEQ_ID = "seq_id"
    MODIFY_NOTE = "modify_note"


quest_post_edit_args = EndpointBase.base_args() | {
    EPQuestPostEditParam.SEQ_ID: fields.Int(default=0),
    EPQuestPostEditParam.TITLE: fields.Str(),
    EPQuestPostEditParam.LANG_CODE: fields.Str(),
    EPQuestPostEditParam.GENERAL_INFO: fields.Str(),
    EPQuestPostEditParam.VIDEO: fields.Str(),
    EPQuestPostEditParam.POSITION_INFO: fields.List(fields.Dict(keys=fields.Str(), values=fields.Str())),
    EPQuestPostEditParam.ADDENDUM: fields.Str(),
    EPQuestPostEditParam.MODIFY_NOTE: fields.Str(),
}


class EPQuestPostEdit(EndpointBase):
    """Endpoint resource to get a post."""

    @use_args(quest_post_edit_args)
    def post(self, args):
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostEditParam.GOOGLE_UID])
        if not is_user_admin:
            return QuestPostPublishFailedResponse(ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        seq_id = args[EPQuestPostEditParam.SEQ_ID]
        title = args[EPQuestPostEditParam.TITLE]
        lang_code = args[EPQuestPostEditParam.LANG_CODE]
        general_info = args[EPQuestPostEditParam.GENERAL_INFO]
        video = args[EPQuestPostEditParam.VIDEO]
        positional_info = EPQuestPostEditParam.pos_info_to_model_key(args[EPQuestPostEditParam.POSITION_INFO])
        addendum = args[EPQuestPostEditParam.ADDENDUM]
        modify_note = args[EPQuestPostEditParam.MODIFY_NOTE]

        edit_outcome = QuestPostController.edit_post(
            seq_id, title, lang_code, general_info, video, positional_info, addendum, modify_note
        )

        if edit_outcome == UpdateResult.NOT_FOUND:
            return QuestPostEditFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 404

        if edit_outcome == UpdateResult.NO_CHANGE:
            return QuestPostEditSuccessResponse(seq_id), 200

        return QuestPostEditSuccessResponse(seq_id), 200


# endregion


# region Quest Post / ID Check

class EPQuestPostIDCheckParam(EPParamBase):
    """Parameters for the request of checking the ID availability."""

    SEQ_ID = "seq_id"
    LANG_CODE = "lang"


quest_post_id_check_args = EndpointBase.base_args() | {
    EPQuestPostIDCheckParam.SEQ_ID: fields.Int(missing=None),
    EPQuestPostIDCheckParam.LANG_CODE: fields.Str()
}


class EPQuestPostIDCheck(EndpointBase):
    """Endpoint resource to check the ID availability."""

    @use_args(quest_post_id_check_args, location="query")
    def get(self, args):
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPQuestPostIDCheckParam.GOOGLE_UID])
        if not is_user_admin:
            return QuestPostIDCheckResponse(False, False), 200

        seq_id = args[EPQuestPostIDCheckParam.SEQ_ID]
        lang_code = args[EPQuestPostIDCheckParam.LANG_CODE]
        available = QuestPostController.is_id_lang_available(seq_id, lang_code)

        return QuestPostIDCheckResponse(is_user_admin, available), 200

# endregion
