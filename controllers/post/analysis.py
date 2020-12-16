"""Unit analysis post data controllers."""
from datetime import datetime
from enum import IntEnum
from typing import Any, Optional

from controllers.base import ModifiableDataKey, MultilingualPostController, MultilingualPostKey
from controllers.results import UpdateResult

__all__ = ("UnitAnalysisPostType", "UnitAnalysisPostKey", "UnitAnalysisPostController")

DB_NAME = "post"


class UnitAnalysisPostType(IntEnum):
    """Type of the unit analysis post."""

    CHARACTER = 1
    DRAGON = 2


class UnitAnalysisPostKey(ModifiableDataKey, MultilingualPostKey):
    """Keys for a single unit analysis post."""

    # Keys for all types

    TYPE = "tp"
    UNIT_NAME = "t"

    SUMMARY = "sm"
    SUMMON_RESULT = "r"

    PASSIVES = "p"
    NORMAL_ATTACKS = "na"

    # ---- (Specific keys here)

    VIDEOS = "v"

    STORY = "st"

    KEYWORDS = "k"

    # Keys for characters

    C_FORCE_STRIKES = "fs"

    C_SKILLS = "sk"

    # ---- Keys for skills

    C_SKILL_NAME = "n"
    C_SKILL_INFO = "i"
    C_SKILL_ROTATIONS = "rt"
    C_SKILL_TIPS = "ts"

    C_TIPS_N_BUILDS = "tb"

    # Keys for dragons

    D_ULTIMATE = "ult"
    D_NOTES = "n"

    D_SUITABLE_CHARACTERS = "sc"

    @classmethod
    def is_c_skill_data_completed(cls, c_skill_data: dict[str, str]) -> bool:
        """Check if ``c_skill_data`` has all the required keys."""
        return c_skill_data.keys() == {cls.C_SKILL_NAME, cls.C_SKILL_INFO, cls.C_SKILL_ROTATIONS, cls.C_SKILL_TIPS}


class _UnitAnalysisPostController(MultilingualPostController):
    """Unit analysis post data controller."""

    database_name = DB_NAME
    collection_name = "analysis"

    def __init__(self):
        super().__init__(UnitAnalysisPostKey)

    def get_posts(
            self, lang_code: str, /, start: int = 0, limit: int = 0
    ) -> tuple[list[dict[str, Any]], int]:
        """
        Get the posts sorted by the last modified date DESC and the total post count.

        This method only returns key information of posts like sequential id (``s``), title (``t``), last modified
        timestamp (``d_m``) and published timestamp (``d_p``).

        :param lang_code: language code
        :param start: starting index of the result
        :param limit: maximum count of the results to be returned
        :return: list of post records
        """
        projection = {
            UnitAnalysisPostKey.SEQ_ID: 1,
            UnitAnalysisPostKey.LANG_CODE: 1,
            UnitAnalysisPostKey.TYPE: 1,
            UnitAnalysisPostKey.UNIT_NAME: 1,
            UnitAnalysisPostKey.DT_LAST_MODIFIED: 1,
            UnitAnalysisPostKey.DT_PUBLISHED: 1,
            UnitAnalysisPostKey.VIEW_COUNT: 1
        }

        return self._get_post_list(lang_code, projection, start=start, limit=limit)

    def publish_chara_post(
            self, unit_name: str, lang_code: str, summary: str, summon_result: str, passives: str,
            normal_attacks: str, special_fs: str, skills: [dict[str, str], dict[str, str]], tips_n_builds: str,
            videos: str, story: str, keywords: str, /,
            seq_id: Optional[int] = None) -> int:
        """
        Publish a character analysis post and get its sequential ID.

        Data in ``skills`` should be insertion-ready (i.e. the keys of each data is already using the key
        from the data model).

        If ``seq_id`` is not specified, a new sequential ID will be used. Otherwise, use the given one.

        :param unit_name: name of the character
        :param lang_code: language code of the post
        :param summary: summary for the character analysis
        :param summon_result: summon result of the corresponding character
        :param passives: passives of the character
        :param normal_attacks: normal attack module of the character
        :param special_fs: special force strike of the character
        :param skills: skills of the character
        :param tips_n_builds: tips and builds for the character
        :param videos: related video for the character analysis
        :param story: story of the character
        :param keywords: keywords of the character analysis post
        :param seq_id: sequential ID of the post
        :return: sequential ID of the newly published post
        :raises ValueError: skill data (`skills`) is incomplete or not using the model key
        """
        # pylint: disable=too-many-arguments, too-many-locals

        new_seq_id = seq_id or self.get_next_seq_id()
        now = datetime.utcnow()

        if any(not UnitAnalysisPostKey.is_c_skill_data_completed(skill) for skill in skills):
            raise ValueError("Incomplete skill data")

        self.insert_one({
            UnitAnalysisPostKey.SEQ_ID: new_seq_id,
            UnitAnalysisPostKey.LANG_CODE: lang_code,
            UnitAnalysisPostKey.TYPE: UnitAnalysisPostType.CHARACTER,
            UnitAnalysisPostKey.UNIT_NAME: unit_name,
            UnitAnalysisPostKey.SUMMARY: summary,
            UnitAnalysisPostKey.SUMMON_RESULT: summon_result,
            UnitAnalysisPostKey.PASSIVES: passives,
            UnitAnalysisPostKey.NORMAL_ATTACKS: normal_attacks,
            UnitAnalysisPostKey.C_FORCE_STRIKES: special_fs,
            UnitAnalysisPostKey.C_SKILLS: skills,
            UnitAnalysisPostKey.C_TIPS_N_BUILDS: tips_n_builds,
            UnitAnalysisPostKey.VIDEOS: videos,
            UnitAnalysisPostKey.STORY: story,
            UnitAnalysisPostKey.VIEW_COUNT: 0,
            UnitAnalysisPostKey.KEYWORDS: keywords,
            UnitAnalysisPostKey.MODIFY_NOTES: [],
            UnitAnalysisPostKey.DT_LAST_MODIFIED: now,
            UnitAnalysisPostKey.DT_PUBLISHED: now,
        })

        return new_seq_id

    def publish_dragon_post(
            self, unit_name: str, lang_code: str, summary: str, summon_result: str, passives: str,
            normal_attacks: str, ultimate: str, notes: str, suitable_characters: str,
            videos: str, story: str, keywords: str, /,
            seq_id: Optional[int] = None) -> int:
        """
        Publish a dragon analysis post and get its sequential ID.

        :param unit_name: name of the dragon
        :param lang_code: language code of the post
        :param summary: summary for the dragon analysis
        :param summon_result: summon result of the corresponding dragon
        :param passives: passives of the dragon
        :param normal_attacks: normal attack module of the dragon
        :param ultimate: special force strike of the dragon
        :param notes: skills of the dragon
        :param suitable_characters: tips and builds for the dragon
        :param videos: related video for the dragon analysis
        :param story: story of the dragon
        :param keywords: keywords of the dragon analysis post
        :param seq_id: sequential ID of the post
        :return: sequential ID of the newly published post
        """
        # pylint: disable=too-many-arguments, too-many-locals

        new_seq_id = seq_id or self.get_next_seq_id()
        now = datetime.utcnow()

        self.insert_one({
            UnitAnalysisPostKey.SEQ_ID: new_seq_id,
            UnitAnalysisPostKey.LANG_CODE: lang_code,
            UnitAnalysisPostKey.TYPE: UnitAnalysisPostType.DRAGON,
            UnitAnalysisPostKey.UNIT_NAME: unit_name,
            UnitAnalysisPostKey.SUMMARY: summary,
            UnitAnalysisPostKey.SUMMON_RESULT: summon_result,
            UnitAnalysisPostKey.PASSIVES: passives,
            UnitAnalysisPostKey.NORMAL_ATTACKS: normal_attacks,
            UnitAnalysisPostKey.D_ULTIMATE: ultimate,
            UnitAnalysisPostKey.D_NOTES: notes,
            UnitAnalysisPostKey.D_SUITABLE_CHARACTERS: suitable_characters,
            UnitAnalysisPostKey.VIDEOS: videos,
            UnitAnalysisPostKey.STORY: story,
            UnitAnalysisPostKey.VIEW_COUNT: 0,
            UnitAnalysisPostKey.KEYWORDS: keywords,
            UnitAnalysisPostKey.MODIFY_NOTES: [],
            UnitAnalysisPostKey.DT_LAST_MODIFIED: now,
            UnitAnalysisPostKey.DT_PUBLISHED: now,
        })

        return new_seq_id

    def edit_chara_post(
            self, seq_id: int, unit_name: str, lang_code: str, summary: str, summon_result: str, passives: str,
            normal_attacks: str, special_fs: str, skills: [dict[str, str], dict[str, str]], tips_n_builds: str,
            videos: str, story: str, keywords: str, modify_note: str) -> UpdateResult:
        """
        Edit a character analysis post.

        Data in ``skills`` should be insertion-ready (i.e. the keys of each data is already using the key
        from the data model).

        :param seq_id: sequential ID of the post
        :param unit_name: name of the character
        :param lang_code: language code of the post
        :param summary: summary for the character analysis
        :param summon_result: summon result of the corresponding character
        :param passives: passives of the character
        :param normal_attacks: normal attack module of the character
        :param special_fs: special force strike of the character
        :param skills: skills of the character
        :param tips_n_builds: tips and builds for the character
        :param videos: related video for the character analysis
        :param story: story of the character
        :param keywords: keywords of the character analysis post
        :param modify_note: modification note
        :return: sequential ID of the newly published post
        :raises ValueError: skill data (`skills`) is incomplete or not using the model key
        """
        # pylint: disable=too-many-arguments, too-many-locals

        return self.update_post(
            seq_id,
            lang_code,
            {
                UnitAnalysisPostKey.UNIT_NAME: unit_name,
                UnitAnalysisPostKey.SUMMARY: summary,
                UnitAnalysisPostKey.SUMMON_RESULT: summon_result,
                UnitAnalysisPostKey.PASSIVES: passives,
                UnitAnalysisPostKey.NORMAL_ATTACKS: normal_attacks,
                UnitAnalysisPostKey.C_FORCE_STRIKES: special_fs,
                UnitAnalysisPostKey.C_SKILLS: skills,
                UnitAnalysisPostKey.C_TIPS_N_BUILDS: tips_n_builds,
                UnitAnalysisPostKey.VIDEOS: videos,
                UnitAnalysisPostKey.STORY: story,
                UnitAnalysisPostKey.KEYWORDS: keywords,
            },
            modify_note,
            addl_update_cond={UnitAnalysisPostKey.TYPE: UnitAnalysisPostType.CHARACTER}
        )

    def edit_dragon_post(
            self, seq_id: int, unit_name: str, lang_code: str, summary: str, summon_result: str, passives: str,
            normal_attacks: str, ultimate: str, notes: str, suitable_characters: str,
            videos: str, story: str, keywords: str, modify_note: str) -> UpdateResult:
        """
        Edit a dragon analysis post.

        :param seq_id: sequential ID of the post
        :param unit_name: name of the dragon
        :param lang_code: language code of the post
        :param summary: summary for the dragon analysis
        :param summon_result: summon result of the corresponding dragon
        :param passives: passives of the dragon
        :param normal_attacks: normal attack module of the dragon
        :param ultimate: special force strike of the dragon
        :param notes: skills of the dragon
        :param suitable_characters: tips and builds for the dragon
        :param videos: related video for the dragon analysis
        :param story: story of the dragon
        :param keywords: keywords of the dragon analysis post
        :param modify_note: modification note
        :return: sequential ID of the newly published post
        """
        # pylint: disable=too-many-arguments, too-many-locals

        return self.update_post(
            seq_id,
            lang_code,
            {
                UnitAnalysisPostKey.UNIT_NAME: unit_name,
                UnitAnalysisPostKey.SUMMARY: summary,
                UnitAnalysisPostKey.SUMMON_RESULT: summon_result,
                UnitAnalysisPostKey.PASSIVES: passives,
                UnitAnalysisPostKey.NORMAL_ATTACKS: normal_attacks,
                UnitAnalysisPostKey.D_ULTIMATE: ultimate,
                UnitAnalysisPostKey.D_NOTES: notes,
                UnitAnalysisPostKey.D_SUITABLE_CHARACTERS: suitable_characters,
                UnitAnalysisPostKey.VIDEOS: videos,
                UnitAnalysisPostKey.STORY: story,
                UnitAnalysisPostKey.KEYWORDS: keywords,
            },
            modify_note,
            addl_update_cond={UnitAnalysisPostKey.TYPE: UnitAnalysisPostType.DRAGON}
        )


UnitAnalysisPostController = _UnitAnalysisPostController()
