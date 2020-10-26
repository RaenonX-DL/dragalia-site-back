from flask import url_for

from endpoints import EPUserLoginParam, EPQuestPostListParam, EPQuestPostGetParam
from responses import Response, ResponseCodeCollection, QuestPostListResponseKey


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

    assert response == Response(ResponseCodeCollection.SUCCESS).serialize()


def test_quest_posts_list(client):
    r = client.get(
        url_for("posts.quest.list"),
        json={
            EPQuestPostListParam.GOOGLE_UID: "Test",
            EPQuestPostListParam.START: 0,
            EPQuestPostListParam.LIMIT: 30
        }
    )

    assert r.status_code == 200

    response = r.json

    assert not response[QuestPostListResponseKey.IS_ADMIN]
    assert response[QuestPostListResponseKey.SUCCESS]
    assert response[QuestPostListResponseKey.CODE] == ResponseCodeCollection.SUCCESS.code


def test_quests_post_get(client):
    r = client.get(
        url_for("posts.quest.get"),
        json={
            EPQuestPostGetParam.GOOGLE_UID: "Test",
            EPQuestPostGetParam.SEQ_ID: 1,
            EPQuestPostGetParam.LANG_CODE: "cht"
        }
    )

    assert r.status_code == 200

    response = r.json

    assert not response[QuestPostListResponseKey.IS_ADMIN]
    assert response[QuestPostListResponseKey.SUCCESS]
    assert response[QuestPostListResponseKey.CODE] == ResponseCodeCollection.SUCCESS.code
