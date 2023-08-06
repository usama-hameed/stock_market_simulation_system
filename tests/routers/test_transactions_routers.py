from fastapi.testclient import TestClient
from apis.routers import app
from db.models import Transactions
from db.connection import session

client = TestClient(app)


def test_create_transactions_success():
    transactions_data = {
        "transaction_id": 1,
        "user_id": 123,
        "ticker": "AAPL",
        "transaction_type": "buy",
        "transaction_price": 150.00,
        "timestamp": "2023-08-06T12:00:00Z"
    }

    response = client.post("/transactions", json=transactions_data)
    assert response.status_code == 200

    created_transactions = response.json()
    assert "transaction_id" in created_transactions
    assert created_transactions["user_id"] == transactions_data["user_id"]
    assert created_transactions["ticker"] == transactions_data["ticker"]
    assert created_transactions["transaction_type"] == transactions_data["transaction_type"]
    assert created_transactions["transaction_price"] == transactions_data["transaction_price"]
    assert created_transactions["timestamp"] == transactions_data["timestamp"]

    db_transactions = session.query(Transactions).filter_by(transaction_id=transactions_data["transaction_id"]).first()
    assert db_transactions is not None
    assert db_transactions.user_id == transactions_data["user_id"]
    assert db_transactions.ticker == transactions_data["ticker"]
    assert db_transactions.transaction_type == transactions_data["transaction_type"]
    assert db_transactions.transaction_price == transactions_data["transaction_price"]
    assert db_transactions.timestamp == transactions_data["timestamp"]


def test_get_transactions_success():
    # Create a transaction in the database
    transaction_data = {
        "transaction_id": 1,
        "user_id": 123,
        "ticker": "AAPL",
        "transaction_type": "buy",
        "transaction_price": 150.00,
        "timestamp": "2023-08-06T12:00:00Z"
    }
    db_transaction = Transactions(**transaction_data)
    session.add(db_transaction)
    session.commit()

    response = client.get(f"/transactions/{transaction_data['user_id']}")
    assert response.status_code == 200

    transaction_response = response.json()
    assert transaction_response["transaction_id"] == transaction_data["transaction_id"]
    assert transaction_response["user_id"] == transaction_data["user_id"]
    assert transaction_response["ticker"] == transaction_data["ticker"]
    assert transaction_response["transaction_type"] == transaction_data["transaction_type"]
    assert transaction_response["transaction_price"] == transaction_data["transaction_price"]
    assert transaction_response["timestamp"] == transaction_data["timestamp"]


def test_get_transactions_failure():
    non_existent_user_id = 999
    response = client.get(f"/transactions/{non_existent_user_id}")
    assert response.status_code == 404


