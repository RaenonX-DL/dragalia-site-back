"""Endpoints to get the data related to object analysis posts."""
from abc import ABC

from webargs import fields
from webargs.flaskparser import use_args

from controllers import GoogleUserDataController, ObjectAnalysisPostController, ObjectAnalysisPostKey
from controllers.results import UpdateResult
from responses import (
    ResponseCodeCollection,
    AnalysisPostListResponse,
    CharaAnalysisPublishSuccessResponse, CharaAnalysisPublishFailedResponse,
    DragonAnalysisPublishSuccessResponse, DragonAnalysisPublishFailedResponse,
    AnalysisPostGetSuccessResponse, AnalysisPostGetFailedResponse,
    AnalysisPostEditSuccessResponse, AnalysisPostEditFailedResponse,
    AnalysisPostIDCheckResponse
)
from .base import EndpointBase
from .post_base import EPPostListParamBase, EPSinglePostParamBase, EPPostModifyParamBase

__all__ = ("EPCharacterAnalysisPostPublish", "EPDragonAnalysisPostPublish",
           "EPAnalysisPostList", "EPAnalysisPostListParam",
           "EPAnalysisPostGet", "EPAnalysisPostGetParam",
           "EPCharaAnalysisPostEdit", "EPDragonAnalysisPostEdit",
           "EPAnalysisPostIDCheck")


# region Analysis Post Base / Publish

class EPAnalysisPostPublishParam(EPSinglePostParamBase, ABC):
    """Base parameters for the request of publishing a analysis post."""

    OBJECT_NAME = "name"

    SUMMARY = "summary"
    SUMMON_RESULT = "summon"

    PASSIVES = "passives"
    NORMAL_ATTACKS = "normal_attacks"

    VIDEOS = "videos"

    STORY = "story"

    KEYWORDS = "keywords"


analysis_pub_args = EPSinglePostParamBase.base_args() | {
    EPAnalysisPostPublishParam.OBJECT_NAME: fields.Str(),
    EPAnalysisPostPublishParam.SUMMARY: fields.Str(),
    EPAnalysisPostPublishParam.SUMMON_RESULT: fields.Str(),
    EPAnalysisPostPublishParam.PASSIVES: fields.Str(),
    EPAnalysisPostPublishParam.NORMAL_ATTACKS: fields.Str(),
    EPAnalysisPostPublishParam.VIDEOS: fields.Str(),
    EPAnalysisPostPublishParam.STORY: fields.Str(),
    EPAnalysisPostPublishParam.KEYWORDS: fields.Str(),
}


# endregion


# region Character Analysis Post / Publish

class EPCharaAnalysisPostPublishParam(EPAnalysisPostPublishParam):
    """Parameters for the request of publishing a character analysis post."""

    FORCE_STRIKES = "force_strikes"
    SKILLS = "skills"

    # Subfield for skills

    SKILL_NAME = "name"
    SKILL_INFO = "info"
    SKILL_ROTATIONS = "rotations"
    SKILL_TIPS = "tips"

    TIPS_N_BUILDS = "tips_builds"

    @classmethod
    def skill_to_model_key(cls, skills: [dict[str, str], dict[str, str]]) -> [dict[str, str], dict[str, str]]:
        """
        Change the skill data to use model key.

        :param skills: skill data to replace the key
        :return: skill data using model key
        """
        ret = []

        for skill in skills:
            ret.append({
                ObjectAnalysisPostKey.C_SKILL_NAME: skill[cls.SKILL_NAME],
                ObjectAnalysisPostKey.C_SKILL_INFO: skill[cls.SKILL_INFO],
                ObjectAnalysisPostKey.C_SKILL_TIPS: skill[cls.SKILL_TIPS],
                ObjectAnalysisPostKey.C_SKILL_ROTATIONS: skill[cls.SKILL_ROTATIONS],
            })

        return ret


chara_analysis_pub_args = analysis_pub_args | {
    EPCharaAnalysisPostPublishParam.FORCE_STRIKES: fields.Str(),
    EPCharaAnalysisPostPublishParam.SKILLS: fields.List(fields.Dict(keys=fields.Str(), values=fields.Str())),
    EPCharaAnalysisPostPublishParam.TIPS_N_BUILDS: fields.Str(),
}


class EPCharacterAnalysisPostPublish(EndpointBase):
    """Endpoint resource to publish a character analysis post."""

    @use_args(chara_analysis_pub_args)
    def post(self, args):  # pylint: disable=no-self-use, missing-function-docstring, too-many-locals
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPCharaAnalysisPostPublishParam.GOOGLE_UID])
        if not is_user_admin:
            return CharaAnalysisPublishFailedResponse(ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        seq_id = args[EPCharaAnalysisPostPublishParam.SEQ_ID]
        object_name = args[EPCharaAnalysisPostPublishParam.OBJECT_NAME]
        lang_code = args[EPCharaAnalysisPostPublishParam.LANG_CODE]
        summary = args[EPCharaAnalysisPostPublishParam.SUMMARY]
        summon_result = args[EPCharaAnalysisPostPublishParam.SUMMON_RESULT]
        passives = args[EPCharaAnalysisPostPublishParam.PASSIVES]
        normal_attacks = args[EPCharaAnalysisPostPublishParam.NORMAL_ATTACKS]
        special_fs = args[EPCharaAnalysisPostPublishParam.FORCE_STRIKES]
        skills = EPCharaAnalysisPostPublishParam.skill_to_model_key(args[EPCharaAnalysisPostPublishParam.SKILLS])
        tips_n_builds = args[EPCharaAnalysisPostPublishParam.TIPS_N_BUILDS]
        videos = args[EPCharaAnalysisPostPublishParam.VIDEOS]
        story = args[EPCharaAnalysisPostPublishParam.STORY]
        keywords = args[EPCharaAnalysisPostPublishParam.KEYWORDS]

        new_seq_id = ObjectAnalysisPostController.publish_chara_post(
            object_name, lang_code, summary, summon_result, passives, normal_attacks, special_fs, skills,
            tips_n_builds, videos, story, keywords, seq_id=seq_id
        )

        return CharaAnalysisPublishSuccessResponse(new_seq_id), 200


# endregion


# region Analysis Analysis Post / Publish

class EPDragonAnalysisPostPublishParam(EPAnalysisPostPublishParam):
    """Parameters for the request of publishing a dragon analysis post."""

    ULTIMATE = "ultimate"
    NOTES = "notes"
    SUITABLE_CHARACTERS = "suitable_characters"


dragon_analysis_pub_args = analysis_pub_args | {
    EPDragonAnalysisPostPublishParam.ULTIMATE: fields.Str(),
    EPDragonAnalysisPostPublishParam.NOTES: fields.Str(),
    EPDragonAnalysisPostPublishParam.SUITABLE_CHARACTERS: fields.Str(),
}


class EPDragonAnalysisPostPublish(EndpointBase):
    """Endpoint resource to publish a dragon analysis post."""

    @use_args(dragon_analysis_pub_args)
    def post(self, args):  # pylint: disable=no-self-use, missing-function-docstring, too-many-locals
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPDragonAnalysisPostPublishParam.GOOGLE_UID])
        if not is_user_admin:
            return DragonAnalysisPublishFailedResponse(
                ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        seq_id = args[EPDragonAnalysisPostPublishParam.SEQ_ID]
        object_name = args[EPDragonAnalysisPostPublishParam.OBJECT_NAME]
        lang_code = args[EPDragonAnalysisPostPublishParam.LANG_CODE]
        summary = args[EPDragonAnalysisPostPublishParam.SUMMARY]
        summon_result = args[EPDragonAnalysisPostPublishParam.SUMMON_RESULT]
        passives = args[EPDragonAnalysisPostPublishParam.PASSIVES]
        normal_attacks = args[EPDragonAnalysisPostPublishParam.NORMAL_ATTACKS]
        ultimate = args[EPDragonAnalysisPostPublishParam.ULTIMATE]
        notes = args[EPDragonAnalysisPostPublishParam.NOTES]
        suitable_characters = args[EPDragonAnalysisPostPublishParam.SUITABLE_CHARACTERS]
        videos = args[EPDragonAnalysisPostPublishParam.VIDEOS]
        story = args[EPDragonAnalysisPostPublishParam.STORY]
        keywords = args[EPDragonAnalysisPostPublishParam.KEYWORDS]

        new_seq_id = ObjectAnalysisPostController.publish_dragon_post(
            object_name, lang_code, summary, summon_result, passives, normal_attacks, ultimate, notes,
            suitable_characters, videos, story, keywords, seq_id=seq_id
        )

        return DragonAnalysisPublishSuccessResponse(new_seq_id), 200


# endregion


# region Analysis Post / List

class EPAnalysisPostListParam(EPPostListParamBase):
    """Parameters for the request of a list of analysis posts."""


analysis_post_list_args = EPPostListParamBase.base_args()


class EPAnalysisPostList(EndpointBase):
    """Endpoint resource to get a quest post list."""

    @use_args(analysis_post_list_args, location="query")
    def get(self, args):  # pylint: disable=no-self-use, missing-function-docstring
        start_idx = args[EPAnalysisPostListParam.START]

        is_user_admin = GoogleUserDataController.is_user_admin(args[EPAnalysisPostListParam.GOOGLE_UID])
        lang_code = args[EPAnalysisPostListParam.LANG_CODE]
        posts, post_count = ObjectAnalysisPostController.get_posts(
            lang_code, start=start_idx, limit=args[EPAnalysisPostListParam.LIMIT]
        )

        return AnalysisPostListResponse(is_user_admin, posts, start_idx, post_count), 200


# endregion


# region Analysis Post / Get

class EPAnalysisPostGetParam(EPSinglePostParamBase):
    """Parameters for the request of getting a analysis post."""

    INCREASE_COUNT = "inc_count"


analysis_post_get_args = EPSinglePostParamBase.base_args() | {
    EPAnalysisPostGetParam.INCREASE_COUNT: fields.Bool()
}


class EPAnalysisPostGet(EndpointBase):
    """Endpoint resource to get a analysis post."""

    @use_args(analysis_post_get_args, location="query")
    def get(self, args):  # pylint: disable=no-self-use, missing-function-docstring
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPAnalysisPostGetParam.GOOGLE_UID])

        seq_id = args[EPAnalysisPostGetParam.SEQ_ID]
        lang_code = args[EPAnalysisPostGetParam.LANG_CODE]
        increase_count = args[EPAnalysisPostGetParam.INCREASE_COUNT]
        result = ObjectAnalysisPostController.get_post(seq_id, lang_code, increase_count)

        if not result.data:
            return AnalysisPostGetFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 404

        return AnalysisPostGetSuccessResponse(is_user_admin, result), 200


# endregion


# region Character Analysis Post / Edit

class EPCharaAnalysisPostEditParam(EPPostModifyParamBase, EPCharaAnalysisPostPublishParam):
    """Parameters for the request of editing a character analysis post."""


chara_analysis_post_edit_args = chara_analysis_pub_args | EPPostModifyParamBase.base_args()


class EPCharaAnalysisPostEdit(EndpointBase):
    """Endpoint resource to edit a character analysis post."""

    @use_args(chara_analysis_post_edit_args)
    def post(self, args):  # pylint: disable=no-self-use, missing-function-docstring, too-many-locals, duplicate-code
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPCharaAnalysisPostEditParam.GOOGLE_UID])
        if not is_user_admin:
            return CharaAnalysisPublishFailedResponse(ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        seq_id = args[EPCharaAnalysisPostEditParam.SEQ_ID]
        object_name = args[EPCharaAnalysisPostEditParam.OBJECT_NAME]
        lang_code = args[EPCharaAnalysisPostEditParam.LANG_CODE]
        summary = args[EPCharaAnalysisPostEditParam.SUMMARY]
        summon_result = args[EPCharaAnalysisPostEditParam.SUMMON_RESULT]
        passives = args[EPCharaAnalysisPostEditParam.PASSIVES]
        normal_attacks = args[EPCharaAnalysisPostEditParam.NORMAL_ATTACKS]
        special_fs = args[EPCharaAnalysisPostEditParam.FORCE_STRIKES]
        skills = EPCharaAnalysisPostEditParam.skill_to_model_key(args[EPCharaAnalysisPostEditParam.SKILLS])
        tips_n_builds = args[EPCharaAnalysisPostEditParam.TIPS_N_BUILDS]
        videos = args[EPCharaAnalysisPostEditParam.VIDEOS]
        story = args[EPCharaAnalysisPostEditParam.STORY]
        keywords = args[EPCharaAnalysisPostEditParam.KEYWORDS]
        modify_note = args[EPCharaAnalysisPostEditParam.MODIFY_NOTE]

        edit_outcome = ObjectAnalysisPostController.edit_chara_post(
            seq_id, object_name, lang_code, summary, summon_result, passives, normal_attacks, special_fs, skills,
            tips_n_builds, videos, story, keywords, modify_note
        )

        if edit_outcome == UpdateResult.NOT_FOUND:
            return CharaAnalysisPublishFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 404

        if edit_outcome == UpdateResult.NO_CHANGE:
            return CharaAnalysisPublishSuccessResponse(seq_id), 200

        return CharaAnalysisPublishSuccessResponse(seq_id), 200


# endregion


# region Dragon Analysis Post / Edit

class EPDragonAnalysisPostEditParam(EPPostModifyParamBase, EPDragonAnalysisPostPublishParam):
    """Parameters for the request of editing a dragon analysis post."""


dragon_analysis_post_edit_args = dragon_analysis_pub_args | EPPostModifyParamBase.base_args()


class EPDragonAnalysisPostEdit(EndpointBase):
    """Endpoint resource to edit a dragon analysis post."""

    @use_args(dragon_analysis_post_edit_args)
    def post(self, args):  # pylint: disable=no-self-use, missing-function-docstring, too-many-locals
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPDragonAnalysisPostEditParam.GOOGLE_UID])
        if not is_user_admin:
            return DragonAnalysisPublishFailedResponse(
                ResponseCodeCollection.FAILED_QUEST_NOT_PUBLISHED_NOT_ADMIN), 401

        seq_id = args[EPDragonAnalysisPostEditParam.SEQ_ID]
        object_name = args[EPDragonAnalysisPostEditParam.OBJECT_NAME]
        lang_code = args[EPDragonAnalysisPostEditParam.LANG_CODE]
        summary = args[EPDragonAnalysisPostEditParam.SUMMARY]
        summon_result = args[EPDragonAnalysisPostEditParam.SUMMON_RESULT]
        passives = args[EPDragonAnalysisPostEditParam.PASSIVES]
        normal_attacks = args[EPDragonAnalysisPostEditParam.NORMAL_ATTACKS]
        ultimate = args[EPDragonAnalysisPostEditParam.ULTIMATE]
        notes = args[EPDragonAnalysisPostEditParam.NOTES]
        suitable_characters = args[EPDragonAnalysisPostEditParam.SUITABLE_CHARACTERS]
        videos = args[EPDragonAnalysisPostEditParam.VIDEOS]
        story = args[EPDragonAnalysisPostEditParam.STORY]
        keywords = args[EPDragonAnalysisPostEditParam.KEYWORDS]
        modify_note = args[EPDragonAnalysisPostEditParam.MODIFY_NOTE]

        edit_outcome = ObjectAnalysisPostController.edit_dragon_post(
            seq_id, object_name, lang_code, summary, summon_result, passives, normal_attacks, ultimate, notes,
            suitable_characters, videos, story, keywords, modify_note
        )

        if edit_outcome == UpdateResult.NOT_FOUND:
            return AnalysisPostEditFailedResponse(ResponseCodeCollection.FAILED_POST_NOT_EXISTS), 404

        if edit_outcome == UpdateResult.NO_CHANGE:
            return AnalysisPostEditSuccessResponse(seq_id), 200

        return AnalysisPostEditSuccessResponse(seq_id), 200


# endregion


# region Analysis Post / ID Check

class EPAnalysisPostIDCheckParam(EPSinglePostParamBase):
    """Parameters for the request of checking the ID availability."""


analysis_post_id_check_args = EPSinglePostParamBase.base_args()


class EPAnalysisPostIDCheck(EndpointBase):
    """Endpoint resource to check the ID availability."""

    @use_args(analysis_post_id_check_args, location="query")
    def get(self, args):  # pylint: disable=no-self-use, missing-function-docstring, duplicate-code
        is_user_admin = GoogleUserDataController.is_user_admin(args[EPAnalysisPostIDCheckParam.GOOGLE_UID])
        if not is_user_admin:
            return AnalysisPostIDCheckResponse(False, False), 200

        seq_id = args[EPAnalysisPostIDCheckParam.SEQ_ID]
        lang_code = args[EPAnalysisPostIDCheckParam.LANG_CODE]
        available = ObjectAnalysisPostController.is_id_lang_available(seq_id, lang_code)

        return AnalysisPostIDCheckResponse(is_user_admin, available), 200

# endregion
