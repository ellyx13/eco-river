import redis.asyncio as redis
import config
import json


# initializing the redis instance
r = redis.from_url("redis://redis:6379")

async def send_message(message: dict):
    message = json.dumps(message)
    await r.publish(channel=config.TOPIC_VIDEO,message=message)

