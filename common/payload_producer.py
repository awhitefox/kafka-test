import json
import os

from aiokafka import AIOKafkaProducer

from . import PayloadMessage


class PayloadProducer:
    def __init__(self, loop):
        self._producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=f'{os.getenv("BOOTSTRAP_SERVER")}:9092',
        )

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()

    async def produce(self, topic: str, msg: PayloadMessage) -> None:
        try:
            await self._producer.send_and_wait(topic, json.dumps(msg).encode('utf-8'))
        except Exception as e:
            await self._producer.stop()
            raise e
