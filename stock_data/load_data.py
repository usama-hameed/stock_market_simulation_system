import random
from datetime import datetime
from .kafka import producer


def load_stock_data():
    stock_data = dict()
    stock_data["ticker"] = random.randint(0, 1000)
    stock_data["open_prince"] = random.randint(500, 5000)
    stock_data["class_price"] = random.randint(500, 5000)
    stock_data["low"] = random.randint(500, 5000)
    stock_data["high"] = random.randint(500, 5000)
    stock_data["volume"] = random.randint(500, 5000)
    stock_data['timestamp'] = str(datetime.now())

    producer(stock_data)


load_stock_data()
