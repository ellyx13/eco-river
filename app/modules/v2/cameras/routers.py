from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends, Response
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from fastapi.responses import StreamingResponse
import os
from . import schemas
from .controllers import camera_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/cameras"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/cameras", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get users success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        results = await camera_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=pagination.search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/cameras/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get users success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await camera_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/cameras", status_code=201, responses={201: {"model": schemas.Response, "description": "Register user success"}})
    async def create(self, data: schemas.CreateRequest):
        result = await camera_controllers.create(data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/cameras/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update user success"}})
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await camera_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/cameras/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        results = await camera_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
        return schemas.Response(**results)

    @router.get("/cameras/stream/{link}", status_code=200)
    def stream(self, link: str):
        return StreamingResponse(
            camera_controllers.streaming_camera(link),
            media_type='multipart/x-mixed-replace;boundary=frame'
    )
        
    @router.get("/cameras/stream/{link}/objects", status_code=200, responses={200: {"model": schemas.ObjectListResponse, "description": "Update user success"}})
    async def get_object(self, link: str):
        results = await camera_controllers.get_object(link)
        return schemas.ObjectListResponse(**results)
    

    def iterfile(self, file_path: str):
        with open(file_path, mode="rb") as file_like:
            while chunk := file_like.read(1024 * 1024):  # Đọc video theo chunk 1MB
                yield chunk

    @router.get("/test/stream", status_code=200)
    async def main(self):
        video_path = "/opt/python-projects/app/modules/v2/cameras/Kasm.mp4"  # Đảm bảo file tồn tại và đường dẫn đúng
    
        if not os.path.exists(video_path):
            return Response(status_code=404, content="Video not found")

        return StreamingResponse(self.iterfile(video_path), media_type="video/mp4")

