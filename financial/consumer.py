import json
import time
import logging
import asyncio


from kafka import KafkaConsumer

from decouple import config

from app.resources.model import Invoice


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def connect_consumer() -> KafkaConsumer:
    """
    Kafka consumer instance generator

    Returns:
        KafkaConsumer: Kafka consumer instance
    """
    try:
        return KafkaConsumer(
            config("KAFKA_TOPIC"),
            bootstrap_servers=[config("KAFKA_URI")],
            value_deserializer=lambda item: json.loads(item.decode('utf-8')),
            group_id='invoice'
        )
    except Exception as e:
        logging.error('Failed to check kafka events:', e)
        logging.error('Trying again in few seconds')
        time.sleep(10)
        return connect_consumer()


async def start() -> None:
    """Start consumer loop"""
    consumer = connect_consumer()
    for appointment_data in consumer:
        logging.info(f'Appointment: {appointment_data.value.get("id")}')
        await Invoice.process_appointment(appointment_data.value)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()
