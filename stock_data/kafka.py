import json
from kafka import KafkaProducer, KafkaConsumer


def producer(data):
    producer_obj = KafkaProducer(bootstrap_servers='localhost:9092')
    producer_obj.send('stock', value=json.dumps(data).encode('utf-8'))
    producer_obj.flush()
    print("Message sent successfully")


def consumer():
    consumer_obj = KafkaConsumer('stock', auto_offset_reset='earliest',
                                 bootstrap_servers='localhost:9092',
                                 consumer_timeout_ms=1000)

    for message in consumer_obj:
        yield message.value
