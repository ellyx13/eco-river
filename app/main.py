from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from routers import api_router
from exceptions import CustomException
from fastapi.openapi.utils import get_openapi
from loguru import logger
from config import PATH_LOGS
import sys
from middlewares.v1.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title='API Eco River')



logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>")
logger.add(PATH_LOGS, colorize=False, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>", rotation="100 MB")

app.include_router(api_router)

# Middlewares
# app.add_middleware(AuthenticationMiddleware)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8007",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomException)
async def standard_exception_handler(request: Request, exc: CustomException):
    # Status code 204 (delete) and 304 (not modified) does not require response content
    if exc.status in [304, 204]:
        return Response(status_code=exc.status)
    return JSONResponse(status_code=exc.status, content={"type": exc.type, "title": exc.title, "status": exc.status, "detail": exc.detail})


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(title="FastAPI Base Project", version="0.0.1", routes=app.routes)
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization", "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"}
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            openapi_schema["paths"][path][method]["security"] = [{"Bearer Auth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
