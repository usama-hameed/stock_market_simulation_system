import json
from typing import List

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from .schemas import CreateUserBase, ListUserBase, StockBase, TransactionBase
from db.connection import session
from db.models import User, Transactions, StockData
from stock_data.kafka import consumer
import redis
from datetime import datetime
from data_processing.task import verify_transaction

app = FastAPI()

rd = redis.Redis(host='redis', port=6379, db=0)


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
        raise HTTPException(detail=error, status_code=400)


@app.get('/user/{username}', response_model=ListUserBase)
def get_user(username: str):
    cache = rd.get(username)
    if cache:
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


@app.get('/stocksdata', response_model=List[StockBase])
def list_stocks():
    final = []
    cache = rd.get('stocks')
    if cache:
        return json.loads(cache)

    stocks = session.query(StockData).all()
    if not stocks:
        raise HTTPException(detail="No Stocks Present", status_code=404)
    for stock in stocks:
        var = {
            "ticker": stock.ticker,
            "open_price": stock.open_price,
            "class_price": stock.class_price,
            "low": stock.low,
            "high": stock.high,
            "volume": stock.volume,
            "timestamp": stock.timestamp
        }
        final.append(var)

    final_json = json.dumps(final)

    rd.set('stocks', final_json)
    return final


@app.get('stocks/{ticker}', response_model=StockBase)
def get_stocks(ticker: int):
    stocks = session.query(StockData).filter(StockData.ticker == ticker).first()
    if not stocks:
        raise HTTPException(status_code=404, detail="Stocks Data Not Found")
    else:
        return stocks


@app.post('/transactions')
def create_transactions(transactions: dict):
    verify_transaction.apply_async(args=transactions)
    return {'message': 'Task For Transaction Verification Submitted'}


@app.get('/transactions/{user_id}', response_model=TransactionBase)
def get_transactions(user_id: int):
    transactions = session.query(Transactions).filter(Transactions.user_id == user_id).first()
    if not transactions:
        raise HTTPException(detail="No Transactions found for this user", status_code=404)
    return transactions
