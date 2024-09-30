from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
import cv2

from . import schemas, config
from .services import camera_services
from modules.v2.projects.controllers import projects_controllers
from .exceptions import ErrorCode as CameraErrorCode
import time
import base64
from ultralytics import YOLO


class CameraControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        await projects_controllers.get_by_id(_id=data['project_id'], commons=commons)
        return await self.service.create(data=data, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)
    
    def decode_base64(self, encoded_str: str) -> str:
        # Giải mã chuỗi base64
        decoded_bytes = base64.b64decode(encoded_str)

        # Chuyển bytes thành string
        decoded_str = decoded_bytes.decode('utf-8')

        return decoded_str

    async def determine_category(self, trash_name):
        trash_name_lower = trash_name.lower()

        for category, details in config.categories.items():
            if any(keyword in trash_name_lower for keyword in details["keywords"]):
                return category, details["score"]
    
        return 'unknown', config.categories["unknown"]["score"]
    
    async def streaming_camera(self, link):
        link = self.decode_base64(link)
        print(link)
        camera = cv2.VideoCapture(link)
        model = YOLO(config.MODEL_PATH)
        objects = {}
        while camera.isOpened():
            success, frame = camera.read()
            if not success:
                break
            current_time_msec = camera.get(cv2.CAP_PROP_POS_MSEC)
            current_time_sec = round(current_time_msec / 1000, 1)
            results = model.track(frame, persist=True, verbose=False)
            if results[0].boxes.id is None:
                continue
            # Get track IDs
            track_ids = results[0].boxes.id.int().cpu().tolist()
            boxes = results[0].boxes.xyxy.tolist()
            names = list(results[0].names.values())
            for idx, track_id in enumerate(track_ids, 0):
                if not objects.get(track_id):
                    result = {}
                    result['seconds'] = current_time_sec
                    result['time'] = time.time()
                    result['name'] = names[0]
                    result['category'], result['environment_score'] = await self.determine_category(names[0])
                    box = boxes[idx]
                    x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
                    result['boxes'] = [x1, y1, x2, y2]
                    objects.update({track_id: result})
                    print(objects)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)

    async def get_object(self, link):
        pass

camera_controllers = CameraControllers(controller_name="cameras", service=camera_services)
