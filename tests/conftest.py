import pytest
from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import random
import string
from app.oauth2 import create_acces_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db_tester():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_db_tester

client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_db_tester():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_tester
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    email = "test_" + random.choice(string.ascii_letters) + \
        str(random.randint(1, 1000000)) + '@mail.com'
    user_data = {"email": email, "password": "wordpass"}
    resp = client.post(
        '/users/', json=user_data)

    assert resp.status_code == 201
    new_user = resp.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    email = "test_" + random.choice(string.ascii_letters) + \
        str(random.randint(1, 1000000)) + '@mail.com'
    user_data = {"email": email, "password": "wordpass"}
    resp = client.post(
        '/users/', json=user_data)

    assert resp.status_code == 201
    new_user = resp.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_acces_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    yield client


@pytest.fixture
def test_posts(test_user,test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },  {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    posts = list(map(lambda post: models.Post(**post), posts_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
