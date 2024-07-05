import os
import json
import aiofiles
import config
from io import BytesIO

def safe_open_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

async def read_video(file_path):
    safe_open_file(file_path)
    file_bytes = bytearray()  
    async with aiofiles.open(file_path, 'rb') as in_file:
        while True:  # Đọc cho đến khi không còn dữ liệu
            content = await in_file.read(config.CHUNK_SIZE)  # Đọc từng chunk
            if not content:
                break  # Nếu không còn dữ liệu thì thoát vòng lặp
            file_bytes += content 
    file_object = BytesIO(file_bytes)
    return file_object 


async def analyze_video(message):
    message = json.loads(message)
    file = await read_video(message['file_path'])
    print(file.filename)
    