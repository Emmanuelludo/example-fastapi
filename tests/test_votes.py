# import pytest
# from app import models


# @pytest.fixture()
# def test_vote(test_posts, session, test_user):
#     new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
#     session.add(new_vote)
#     session.commit()


def test_vote_on_post(authorized_client, test_posts):
    resp = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': True})
    assert resp.status_code == 201
    assert resp.json()['message'] == 'successfully added vote'


def test_vote_twice_post(authorized_client, test_posts, test_user):  # test_vote
    resp1 = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': True})
    resp2 = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': True})
    assert resp2.status_code == 409
    assert resp2.json()[
        'detail'] == f"user {test_user['id']} has already voted on post {test_posts[0].id}"


def test_vote_unauth_user(client, test_posts):
    resp = client.post(
        "/votes/", json={"post_id": test_posts[0].id, "voted": True})
    assert resp.status_code == 401
    assert resp.json()['detail'] == 'Not authenticated'


def test_delete_vote(authorized_client, test_posts):  # test_vote
    resp1 = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': True})
    resp = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': False})
    assert resp.status_code == 201
    assert resp.json()['message'] == "successfully deleted vote"


def test_delete_vote_not_exist(authorized_client, test_posts):
    resp = authorized_client.post(
        "/votes/", json={'post_id': test_posts[0].id, 'voted': False})
    assert resp.status_code == 404
    assert resp.json()['detail'] == "Vote does not exist"


def test_vote_no_post(authorized_client, test_posts):
    resp = authorized_client.post(
        "/votes/", json={'post_id': -800, 'voted': False})
    assert resp.status_code == 404
    assert resp.json()[
        'detail'] == f"post with id: -800 not found"
