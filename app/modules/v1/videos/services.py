from fastapi import UploadFile
import publisher
import aiofiles
import os
import config
import time



def safe_open_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


async def write_file(file):
    filename = str(int(time.time())) + '_' + file.filename
    file_path = config.PROJECT_PATH + "/video/" + filename
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(config.CHUNK_SIZE):
            await out_file.write(content)
    return file_path


async def upload_video(file: UploadFile):
    file_path = await write_file(file)
    await publisher.send_message(message={'file_path': file_path})