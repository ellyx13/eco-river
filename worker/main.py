import redis.asyncio as redis
import asyncio
import config
from modules.v1.videos import services as video_services
from loguru import logger
import sys
import json

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>")
logger.add(config.PATH_LOGS, colorize=False, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>", rotation="100 MB")
   
async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            message = json.loads(message['data'])
            await video_services.analyze_video(message=message)
            
            
            
async def main():
    # initializing the redis instance
    r = redis.from_url("redis://redis:6379")
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(config.TOPIC_VIDEO)
        logger.info('Start worker successfully. Waiting for message ...')
        future = asyncio.create_task(reader(pubsub))
        await future
 
    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close() 
