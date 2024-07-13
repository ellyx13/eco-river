from fastapi import UploadFile, HTTPException
import publisher
import aiofiles
import os
from . import config
from config import PROJECT_PATH
import time
from loguru import logger
import random
import uuid
from partners.v1.firebase.services import firebase_video_services

def safe_open_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


async def write_file(file):
    filename = str(int(time.time())) + '_' + file.filename
    file_path = PROJECT_PATH + "/storages/videos/" + filename
    safe_open_file(file_path)
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(config.CHUNK_SIZE):
            await out_file.write(content)
    return file_path, filename


async def upload_video(file: UploadFile):
    file_path, filename = await write_file(file)
    logger.info(f'File path: {file_path}')
    
    data = {'filename': filename, 'status': 'processing'}
    doc = await firebase_video_services.add(data=data)
    await publisher.send_message(message={'file_path': file_path, 'document_id': doc.id})
    result = {}
    result['_id'] = doc.id
    result['status'] = 'success'
    return result



def _generate_coordinates():
    x1 = random.uniform(0, 700)  
    y1 = random.uniform(0, 700)
    x2 = random.uniform(0, 700)
    y2 = random.uniform(0, 700)
    return [x1, y1, x2, y2]

async def generate_fake_data(video_id):
    results = {}
    results['_id'] = video_id
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
        boxes = _generate_coordinates()
        data.append({'name':name, 'category':category, 'environment_score':score, 'seconds':seconds, 'boxes': boxes})
    
    if total_score <= 20:
        pollution_level = "Low"
    elif total_score <= 30:
        pollution_level = "Medium"
    else:
        pollution_level = "High"
    
    results = {}
    results['_id'] = video_id
    results['status'] = 'done'
    results['total_items'] = num_items
    results['total_environment_score'] = total_score
    results['environmental_pollution_level'] = pollution_level
    results['results'] = data
    return results


async def get_video(video_id: str, is_analyzed: bool = False):
    if is_analyzed is True:
        return await generate_fake_data(video_id=video_id)
    item = await firebase_video_services.get_by_id(document_id=video_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Video with id {video_id} could not be found")
    item['_id'] = video_id
    return item
    
    
    
