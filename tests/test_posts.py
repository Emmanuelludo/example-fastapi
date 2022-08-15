from turtle import pos
import pytest
from typing import List
from app import schemas

from app import models


def test_get_all_posts(authorized_client, test_posts):
    resp = authorized_client.get('/posts/')
    assert resp.status_code == 200
    # for item in resp.json():
    #     post = schemas.PostwVotes(**item)
    #     assert post.Post.owner_id == post.Post.owner.id
    posts = list(map(lambda post: schemas.PostwVotes(**post), resp.json()))
    assert len(resp.json()) == len(test_posts)


def test_user_get_one_post(authorized_client, test_posts):
    resp = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert resp.status_code == 200
    post = schemas.PostwVotes(**resp.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_user_get_one_not_post(client, test_posts):
    resp = client.get("/posts/-20")
    assert resp.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("Travelling minstrel", "awesome songs", False),
    ("favorite pizza", "i love pepperoni", True),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    resp = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**resp.json())
    assert resp.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    assert created_post.owner.email == test_user['email']


@pytest.mark.parametrize("title, content", [
    ("Travelling minstrel", "awesome songs"),
    ("favorite pizza", "i love pepperoni"),
])
def test_create_posts_default(authorized_client, title, content):
    resp = authorized_client.post(
        "/posts/", json={"title": title, "content": content})
    created_post = schemas.PostResponse(**resp.json())
    assert resp.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True


@pytest.mark.parametrize("title, content, published", [
    ("Travelling minstrel", "awesome songs", False),
    ("favorite pizza", "i love pepperoni", True),
])
def test_unauth_create_post(client, title, content, published):
    resp = client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    assert resp.status_code == 401


def test_unauth_delete_post(client, test_posts):
    resp = client.delete(
        f"/posts/{test_posts[0].id}")
    assert resp.status_code == 401
    assert resp.json()['detail'] == 'Not authenticated'


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    resp = authorized_client.get('/posts/')
    assert len(resp.json()) == len(test_posts)-1


def test_delete_post_not_exist(authorized_client, test_posts):
    resp = authorized_client.delete(
        "/posts/-120")
    assert resp.status_code == 404
    assert resp.json()['detail'] == "post with id -120 not found"


def test_delete_other_user_post(authorized_client, test_posts):
    resp = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert resp.status_code == 401
    assert resp.json()[
        'detail'] == "Not authorized to perform requested action"


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id

    }
    resp = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert resp.status_code == 200
    updated_post = schemas.PostResponse(**resp.json())
    assert updated_post.title == data['title']


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id

    }
    resp = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert resp.status_code == 401
    assert resp.json()[
        'detail'] == 'Not authorized to perform requested action'


def test_update_non_exist_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",

    }
    resp = authorized_client.put("/posts/-8000", json=data)
    assert resp.status_code == 404
    assert resp.json()[
        'detail'] == 'post with id -8000 does not exist'


def test_unauth_update_post(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",

    }
    resp = client.put("/posts/-8000", json=data)
    assert resp.status_code == 401
    assert resp.json()[
        'detail'] == 'Not authenticated'
