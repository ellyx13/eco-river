from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import projects_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/projects"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/projects", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get users success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["summary"]
        results = await projects_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
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

    @router.get("/projects/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get users success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await projects_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/projects", status_code=201, responses={201: {"model": schemas.Response, "description": "Register user success"}})
    async def create(self, data: schemas.CreateRequest):
        result = await projects_controllers.create(data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/projects/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update user success"}})
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await projects_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/projects/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        results = await projects_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
        return schemas.Response(**results)
