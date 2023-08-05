from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, func, Enum, Sequence
from sqlalchemy.orm import relationship
from .connection import Base
from enum import Enum as PyEnum


class TransactionType(PyEnum):
    BUY = 'buy'
    SELL = 'sell'


class User(Base):
    __tablename__ = 'user_table'

    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True, autoincrement=True)
    username = Column(String,  unique=True, nullable=False, index=True)
    balance = Column(Integer, default=0, nullable=False)

    transactions = relationship('Transactions', back_populates='user', cascade='all, delete-orphan')


class StockData(Base):
    __tablename__ = 'stock_table'

    ticker = Column(Integer, primary_key=True, index=True)
    open_price = Column(Integer)
    class_price = Column(Integer)
    low = Column(Integer)
    high = Column(Integer)
    volume = Column(Integer)
    timestamp = Column(TIMESTAMP, server_default=func.now())


class Transactions(Base):
    __tablename__ = 'transactions_table'

    transaction_id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('user_table.user_id'))
    ticker = Column(Integer)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    transaction_price = Column(Integer)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User', back_populates='transactions')
