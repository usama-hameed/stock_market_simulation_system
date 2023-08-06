import json
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from .schemas import CreateUserBase, ListUserBase
from db.connection import session
from db.models import User, TransactionType, Transactions, StockData
from stock_data.kafka import consumer
import redis
from datetime import datetime

app = FastAPI()

rd = redis.Redis(host='localhost', port=6379, db=0)


@app.post('/user')
def create_user(user: CreateUserBase):
    try:
        user_data = User(username=user.username, balance=user.balance)
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        session.close()
        return user_data
    except Exception as error:
        raise HTTPException(detail=error, status_code=500)


@app.get('/user/{username}', response_model=ListUserBase)
def get_user(username: str):
    cache = rd.get(username)
    if cache:
        print("CACHE HIT")
        return json.loads(cache)
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "balance": user.balance
    }

    user_json = json.dumps(user_data)

    rd.set(username, user_json)

    return user


@app.post('/stocks')
def add_stocks():
    stock_data = consumer()

    for data in stock_data:
        data = json.loads(data)
        data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        stock = StockData(ticker=data['ticker'], open_price=data['open_prince'], class_price=data['class_price'],
                          low=data['low'], high=data['high'], volume=data['volume'])
        session.add(stock)
        session.commit()
        session.refresh(stock)
    return {'message': 'Stock Data saved'}

