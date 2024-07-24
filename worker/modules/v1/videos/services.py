import os
from loguru import logger
from modules.v1.ai import object_counter
from partners.v1.firebase.services import firebase_video_services

def safe_open_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

async def analyze_video(message):
    try:
        logger.info(f"(Video) Message Received: {message}")
        file_path = message['file_path']
        if not os.path.exists(file_path):
            return
        results = await object_counter.analyze_video(file_path=file_path)
        await firebase_video_services.update_by_id(document_id=message['document_id'], data=results)


    except Exception as exc:
        logger.error(f'Analyze video {message["file_path"]} failed because error: {exc}')
        data_update = {'status': 'error'}
        await firebase_video_services.update_by_id(document_id=message['document_id'], data=data_update)
        
    delete_file(message['file_path'])