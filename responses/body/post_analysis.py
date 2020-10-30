"""Response body for getting the data related to object analysis posts."""
from typing import Any

from controllers import MultilingualGetOneResult, ObjectAnalysisPostKey, ObjectAnalysisPostType
from .post_base import (
    PostPublishSuccessResponseKey, PostPublishSuccessResponse, PostPublishFailedResponse,
    PostListResponseKey, PostListResponse,
    PostGetSuccessResponseKey, PostGetSuccessResponse, PostGetFailedResponse,
    PostEditSuccessResponseKey, PostEditSuccessResponse, PostEditFailedResponse,
    PostIDCheckResponse, PostIDCheckResponseKey
)

__all__ = ("CharaAnalysisPublishSuccessResponse", "CharaAnalysisPublishFailedResponse",
           "CharaAnalysisPublishSuccessResponseKey",
           "DragonAnalysisPublishSuccessResponse", "DragonAnalysisPublishFailedResponse",
           "DragonAnalysisPublishSuccessResponseKey",
           "AnalysisPostListResponse", "AnalysisPostListResponseKey",
           "AnalysisPostGetSuccessResponse", "AnalysisPostGetFailedResponse", "AnalysisPostGetSuccessResponseKey",
           "AnalysisPostEditSuccessResponse", "AnalysisPostEditFailedResponse", "AnalysisPostEditSuccessResponseKey",
           "AnalysisPostIDCheckResponseKey", "AnalysisPostIDCheckResponse")


# region Analysis Post (Character) / Publish

class CharaAnalysisPublishSuccessResponseKey(PostPublishSuccessResponseKey):
    """Response keys of successfully published a character analysis post."""


class CharaAnalysisPublishSuccessResponse(PostPublishSuccessResponse):
    """Response body of successfully published a character analysis post."""


class CharaAnalysisPublishFailedResponse(PostPublishFailedResponse):
    """Response body of failed to publish a character analysis post."""


# endregion


# region Analysis Post (Dragon) / Publish

class DragonAnalysisPublishSuccessResponseKey(PostPublishSuccessResponseKey):
    """Response keys of successfully published a character analysis post."""


class DragonAnalysisPublishSuccessResponse(PostPublishSuccessResponse):
    """Response body of successfully published a character analysis post."""


class DragonAnalysisPublishFailedResponse(PostPublishFailedResponse):
    """Response body of failed to publish a character analysis post."""


# endregion


# region Analysis Post / List

class AnalysisPostListResponseKey(PostListResponseKey):
    """
    Response keys of getting an analysis post list.

    Keys must be consistent with the type ``AnalysisPostListResponse`` at the front side.
    """

    # These keys need to be consistent with the definition structure at the front side
    # Type name: `PostListEntry`
    POSTS_SEQ_ID = "seqId"
    POSTS_LANG = "lang"
    POSTS_TYPE = "type"
    POSTS_OBJECT_NAME = "objectName"
    POSTS_LAST_MODIFIED = "modified"
    POSTS_PUBLISHED = "published"
    POSTS_VIEW_COUNT = "viewCount"

    @classmethod
    def convert_posts_key(cls, posts: list[dict[str, Any]]):
        """Convert the keys in ``posts`` from model key to be the keys for the response."""
        ret = []

        for post in posts:
            ret.append({
                cls.POSTS_SEQ_ID: post[ObjectAnalysisPostKey.SEQ_ID],
                cls.POSTS_LANG: post[ObjectAnalysisPostKey.LANG_CODE],
                cls.POSTS_TYPE: post[ObjectAnalysisPostKey.TYPE],
                cls.POSTS_OBJECT_NAME: post[ObjectAnalysisPostKey.OBJECT_NAME],
                cls.POSTS_LAST_MODIFIED: post[ObjectAnalysisPostKey.DT_LAST_MODIFIED],
                cls.POSTS_PUBLISHED: post[ObjectAnalysisPostKey.DT_PUBLISHED],
                cls.POSTS_VIEW_COUNT: post[ObjectAnalysisPostKey.VIEW_COUNT],
            })

        return ret


class AnalysisPostListResponse(PostListResponse):
    """Response body of getting a analysis post list."""

    def __init__(self, is_admin: bool, posts: list[dict[str, Any]], start_idx: int, post_count: int):
        super().__init__(is_admin, start_idx, post_count)

        self._posts = AnalysisPostListResponseKey.convert_posts_key(posts)

    def serialize(self):
        return super().serialize() | {
            AnalysisPostListResponseKey.POSTS: self._posts
        }


# endregion


# region Analysis Post / Get

class AnalysisPostGetSuccessResponseKey(PostGetSuccessResponseKey):
    """
    Response keys of getting a analysis post.

    Keys must be consistent with the type ``AnalysisPostGetResponse`` at the front side.
    """

    TYPE = "type"
    OBJECT_NAME = "name"

    SUMMARY = "summary"
    SUMMON_RESULT = "summonResult"

    PASSIVES = "passives"
    NORMAL_ATTACKS = "normalAttacks"

    # ---- (Specific keys here)

    VIDEOS = "videos"

    STORY = "story"

    KEYWORDS = "keywords"

    # Keys for characters

    C_FORCE_STRIKES = "forceStrikes"

    C_SKILLS = "skills"

    # ---- Keys for skills

    C_SKILL_NAME = "name"
    C_SKILL_INFO = "info"
    C_SKILL_ROTATIONS = "rotations"
    C_SKILL_TIPS = "tips"

    C_TIPS_N_BUILDS = "tipsBuilds"

    # Keys for dragons

    D_ULTIMATE = "ultimate"
    D_NOTES = "notes"

    D_SUITABLE_CHARACTERS = "suitableCharacters"

    @classmethod
    def convert_skill_key(cls, skills: list[dict[str, Any]]):
        """Convert the keys in ``skills`` from model key to be the keys for the response."""
        ret = []

        for skill in skills:
            ret.append({
                cls.C_SKILL_NAME: skill[ObjectAnalysisPostKey.C_SKILL_NAME],
                cls.C_SKILL_INFO: skill[ObjectAnalysisPostKey.C_SKILL_INFO],
                cls.C_SKILL_ROTATIONS: skill[ObjectAnalysisPostKey.C_SKILL_ROTATIONS],
                cls.C_SKILL_TIPS: skill[ObjectAnalysisPostKey.C_SKILL_TIPS],
            })

        return ret


class AnalysisPostGetSuccessResponse(PostGetSuccessResponse):
    """Response body of getting a analysis post."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, is_admin: bool, get_result: MultilingualGetOneResult):
        super().__init__(is_admin, get_result)

        post = get_result.data

        self._type = post[ObjectAnalysisPostKey.TYPE]
        self._object_name = post[ObjectAnalysisPostKey.OBJECT_NAME]
        self._summary = post[ObjectAnalysisPostKey.SUMMARY]
        self._summon_result = post[ObjectAnalysisPostKey.SUMMON_RESULT]
        self._passives = post[ObjectAnalysisPostKey.PASSIVES]
        self._normal_attacks = post[ObjectAnalysisPostKey.NORMAL_ATTACKS]
        self._videos = post[ObjectAnalysisPostKey.VIDEOS]
        self._story = post[ObjectAnalysisPostKey.STORY]
        self._keywords = post[ObjectAnalysisPostKey.KEYWORDS]

        self._type_specific_serialized = {}
        if self._type == ObjectAnalysisPostType.CHARACTER:
            self._type_specific_serialized = {
                AnalysisPostGetSuccessResponseKey.C_FORCE_STRIKES: post[ObjectAnalysisPostKey.C_FORCE_STRIKES],
                AnalysisPostGetSuccessResponseKey.C_SKILLS:
                    AnalysisPostGetSuccessResponseKey.convert_skill_key(post[ObjectAnalysisPostKey.C_SKILLS]),
                AnalysisPostGetSuccessResponseKey.C_TIPS_N_BUILDS: post[ObjectAnalysisPostKey.C_TIPS_N_BUILDS],
            }
        elif self._type == ObjectAnalysisPostType.DRAGON:
            self._type_specific_serialized = {
                AnalysisPostGetSuccessResponseKey.D_ULTIMATE: post[ObjectAnalysisPostKey.D_ULTIMATE],
                AnalysisPostGetSuccessResponseKey.D_NOTES: post[ObjectAnalysisPostKey.D_NOTES],
                AnalysisPostGetSuccessResponseKey.D_SUITABLE_CHARACTERS: post[
                    ObjectAnalysisPostKey.D_SUITABLE_CHARACTERS],
            }

    def serialize(self):
        return super().serialize() | {
            AnalysisPostGetSuccessResponseKey.TYPE: self._type,
            AnalysisPostGetSuccessResponseKey.OBJECT_NAME: self._object_name,
            AnalysisPostGetSuccessResponseKey.SUMMARY: self._summary,
            AnalysisPostGetSuccessResponseKey.SUMMON_RESULT: self._summon_result,
            AnalysisPostGetSuccessResponseKey.PASSIVES: self._passives,
            AnalysisPostGetSuccessResponseKey.NORMAL_ATTACKS: self._normal_attacks,
            AnalysisPostGetSuccessResponseKey.VIDEOS: self._videos,
            AnalysisPostGetSuccessResponseKey.STORY: self._story,
            AnalysisPostGetSuccessResponseKey.KEYWORDS: self._keywords,
        } | self._type_specific_serialized


class AnalysisPostGetFailedResponse(PostGetFailedResponse):
    """Response body of failed to get a analysis post."""


# endregion


# region Analysis Post / Edit

class AnalysisPostEditSuccessResponseKey(PostEditSuccessResponseKey):
    """Response keys of successfully edited a analysis post."""


class AnalysisPostEditSuccessResponse(PostEditSuccessResponse):
    """Response body of successfully edited a analysis post."""


class AnalysisPostEditFailedResponse(PostEditFailedResponse):
    """Response body of failed to edit a analysis post."""


# endregion


# region Analysis Post / ID Check

class AnalysisPostIDCheckResponseKey(PostIDCheckResponseKey):
    """Response keys of a analysis post ID check request."""


class AnalysisPostIDCheckResponse(PostIDCheckResponse):
    """Response body of a analysis post ID check request."""

# endregion
