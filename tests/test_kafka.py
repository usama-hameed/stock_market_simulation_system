import json
import pytest
from stock_data.kafka import producer, consumer


@pytest.fixture
def mock_producer(mocker):
    return mocker.patch('stock_data.kafka.KafkaProducer')


@pytest.fixture
def mock_consumer(mocker):
    return mocker.patch('stock_data.kafka.KafkaConsumer')


def test_producer(mock_producer, mocker):
    data = {"key": "value"}
    mock_send = mocker.MagicMock()
    mock_flush = mocker.MagicMock()
    mock_producer.return_value.send.return_value = mock_send
    mock_producer.return_value.flush = mock_flush

    producer(data)

    mock_send.assert_called_once_with(
        'stock', value=json.dumps(data).encode('utf-8'))
    mock_flush.assert_called_once()


def test_consumer(mock_consumer, mocker):
    mock_message = mocker.MagicMock(value=json.dumps({"key": "value"}).encode('utf-8'))
    mock_consumer_instance = mocker.MagicMock()
    mock_consumer_instance.__iter__.return_value = [mock_message]
    mock_consumer.return_value = mock_consumer_instance

    messages = list(consumer())

    assert len(messages) == 1
    assert messages[0] == mock_message.value
