import json
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from .schemas import UserBase
from db.connection import session
from db.models import User, TransactionType, Transactions, StockData
app = FastAPI()


@app.post('/user')
def create_user(user: UserBase):
    try:
        user_data = User(username=user.username, balance=user.balance)
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        session.close()
        return user_data
    except Exception as error:

        raise HTTPException(detail=error, status_code=400)
