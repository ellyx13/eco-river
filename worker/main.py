import redis.asyncio as redis
import asyncio
import config
from modules.v1.videos import services as video_services

r = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True
)


   
async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Sub) Message Received: {message}")
            
            
async def main():
    r = redis.from_url("redis://localhost")
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(config.TOPIC_VIDEO)
        future = asyncio.create_task(reader(pubsub))
        await future
 
    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close() 
