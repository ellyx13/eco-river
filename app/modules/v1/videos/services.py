from fastapi import UploadFile
import publisher
import aiofiles
import os
from . import config, schemas
from config import PROJECT_PATH
import time
from loguru import logger
import random
from utils import arequest
import uuid

def safe_open_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


async def write_file(file):
    filename = str(int(time.time())) + '_' + file.filename
    file_path = PROJECT_PATH + "/storages/videos/" + filename
    safe_open_file(file_path)
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(config.CHUNK_SIZE):
            await out_file.write(content)
    return file_path


async def upload_video(file: UploadFile):
    file_path = await write_file(file)
    logger.info(f'File path: {file_path}')
    await publisher.send_message(message={'file_path': file_path})
    result = {}
    result['_id'] = str(uuid.uuid4())
    result['status'] = 'success'
    return result


async def get_video(video_id: str, is_analyzed: bool = False):
    results = {}
    results['_id'] = video_id
    
    if is_analyzed is False:
        return results

    pollution_levels = ["Low", "Medium", "High"]
    items = {
        "Plastic Bottle": "Plastic",
        "Metal Can": "Metal",
        "Newspaper": "Paper",
        "Glass Jar": "Glass",
        "Banana Peel": "Organic",
        "Plastic Bag": "Plastic",
        "Aluminum Foil": "Metal",
        "Cardboard Box": "Paper",
        "Glass Bottle": "Glass",
        "Apple Core": "Organic",
        "Styrofoam Cup": "Plastic",
        "Copper Wire": "Metal",
        "Paper Towel": "Paper",
        "Glass Shard": "Glass",
        "Orange Peel": "Organic"
    }
    
    num_items = random.randint(1, 15)
    selected_items = random.sample(list(items.items()), num_items)

    data = []
    total_score = 0
    
    for name, category in selected_items:
        score = random.randint(1, 10)
        seconds = random.randint(1, 600)
        total_score += score
        data.append({'name':name, 'category':category, 'environment_score':score, 'seconds':seconds})
    
    if total_score <= 20:
        pollution_level = "Low"
    elif total_score <= 30:
        pollution_level = "Medium"
    else:
        pollution_level = "High"
    
    results = {}
    results['_id'] = video_id
    results['total_items'] = num_items
    results['total_environment_score'] = total_score
    results['environmental_pollution_level'] = pollution_level
    results['results'] = data
    return results
    
    
    
