from flask import url_for

from endpoints import EPUserLoginParam, EPQuestPostListParam, EPQuestPostGetParam
from responses import ResponseCodeCollection, QuestPostListResponseKey


def test_root(client):
    r = client.get(url_for("misc.root"))

    assert r.status_code == 200

    response = r.json

    assert response[QuestPostListResponseKey.CODE] == ResponseCodeCollection.SUCCESS.code
    assert response[QuestPostListResponseKey.SUCCESS]


def test_user_login(client):
    r = client.post(
        url_for("user.login"),
        json={
            EPUserLoginParam.GOOGLE_UID: "Test",
            EPUserLoginParam.GOOGLE_EMAIL: "Test@gmail.com"
        }
    )

    assert r.status_code == 200

    response = r.json

    assert response[QuestPostListResponseKey.CODE] \
           in (ResponseCodeCollection.SUCCESS.code, ResponseCodeCollection.SUCCESS_NEW.code)
    assert response[QuestPostListResponseKey.SUCCESS]


def test_quest_posts_list(client):
    r = client.get(
        url_for("posts.quest.list"),
        query_string={
            EPQuestPostListParam.GOOGLE_UID: "Test",
            EPQuestPostListParam.START: 0,
            EPQuestPostListParam.LIMIT: 30,
            EPQuestPostListParam.LANG_CODE: "en"
        }
    )

    assert r.status_code == 200

    response = r.json

    assert response[QuestPostListResponseKey.CODE] == ResponseCodeCollection.SUCCESS.code
    assert not response[QuestPostListResponseKey.IS_ADMIN]
    assert response[QuestPostListResponseKey.SUCCESS]


def test_quests_post_get(client):
    r = client.get(
        url_for("posts.quest.get"),
        query_string={
            EPQuestPostGetParam.GOOGLE_UID: "Test",
            EPQuestPostGetParam.SEQ_ID: 99999999999999,
            EPQuestPostGetParam.LANG_CODE: "cht",
            EPQuestPostGetParam.INCREASE_COUNT: 1
        }
    )

    assert r.status_code == 404

    response = r.json

    assert response[QuestPostListResponseKey.CODE] == ResponseCodeCollection.FAILED_POST_NOT_EXISTS.code
    assert not response[QuestPostListResponseKey.SUCCESS]
