from db.connection import session
from db.models import User, Transactions
from .celery_config import celery_app


@celery_app.task
def verify_transaction(transactions):
    user = session.query(User).filter(User.user_id == transactions['user_id']).first()

    if user.balance > transactions['transaction_price']:
        transactions_data = Transactions(transaction_id=transactions["transaction_id"], user_id=transactions["user_id"],
                                         ticker=transactions["ticker"], transaction_type=transactions["transaction_type"],
                                         transaction_price=transactions["transaction_price"],
                                         timestamp=transactions["timestamp"])

        session.add(transactions_data)
        session.commit()
        session.close()
