import json

from kafka import KafkaProducer

from app.conf import settings


def kafka_producer_instance() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[settings.KAFKA_URI],
        value_serializer=lambda item: json.dumps(item).encode('utf-8')
    )
