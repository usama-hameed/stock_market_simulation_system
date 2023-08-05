from pydantic import BaseModel, validator
from datetime import datetime
from db.connection import session
from db.models import User
from sqlalchemy import exists
from fastapi.exceptions import HTTPException


class UserBase(BaseModel):
    # user_id: int
    username: str
    balance: int

    @validator("username")
    def is_username_exist(cls, username):
        username_exists = session.query(exists().where(User.username == username)).scalar()
        if username_exists:
            raise HTTPException(detail="username already exist", status_code=400)
        return username

    class Config:
        orm_mode = True


class StockBase(BaseModel):
    ticker: int
    open_price: int
    class_price: int
    low: int
    high: int
    volume: int
    timestamp: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    transaction_id: int
    user_id: int
    ticker: int
    transaction_type: str
    transaction_price: int
    timestamp: datetime

    class Config:
        orm_mode = True
