import redis.asyncio as redis
import config
import json


# initializing the redis instance
r = redis.from_url("redis://localhost")

async def send_message(message: dict):
    message = json.dumps(message)
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(config.TOPIC_VIDEO)
        await r.publish(message)

