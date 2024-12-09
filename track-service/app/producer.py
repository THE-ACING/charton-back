import json
from typing import AsyncIterable

from aiokafka import AIOKafkaProducer
from dishka import Provider, Scope, provide

from app.settings import Settings


class KafkaProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_kafka_producer(self, settings: Settings) -> AsyncIterable[AIOKafkaProducer]:
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        try:
            await producer.start()
            yield producer
        finally:
            await producer.stop()