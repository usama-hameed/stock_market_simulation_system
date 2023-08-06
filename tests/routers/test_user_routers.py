from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from apis.routers import app
from db.models import User
from db.connection import session

client = TestClient(app)


def test_create_user_success():
    user_data = {
        "username": "test1",
        "balance": 100
    }

    response = client.post("/user", json=user_data)
    assert response.status_code == 200

    created_user = response.json()
    assert "user_id" in created_user
    assert created_user["username"] == user_data["username"]
    assert created_user["balance"] == user_data["balance"]

    db_user = session.query(User).filter_by(username=user_data["username"]).first()
    assert db_user is not None
    assert db_user.balance == user_data["balance"]


def test_create_user_failure():
    user_data = {
        "username": "test"
    }

    response = client.post("/user", json=user_data)
    assert response.status_code == 400


def test_get_existing_user():
    user_data = {
        "username": "usamahameed@1997",
        "balance": 100
    }
    user = User(username=user_data['username'], balance=user_data['balance'])
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get("/user/usamahameed@1997")
    assert response.status_code == 200
    assert response.json()['username'] == 'usamahameed@1997'
    assert response.json()['balance'] == 100


def test_not_existing_user():
    response = client.get("/user/xyz")

    assert response.status_code == 404
