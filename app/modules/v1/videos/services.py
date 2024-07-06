from fastapi import UploadFile
import publisher
import aiofiles
import os
from . import config
from config import PROJECT_PATH
import time
from loguru import logger


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