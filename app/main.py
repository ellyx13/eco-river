from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import api_router
from exception import UnicornException
from loguru import logger
from config import PATH_LOGS
import sys


app = FastAPI(title='API Eco River')



logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>")
logger.add(PATH_LOGS, colorize=False, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>", rotation="100 MB")

app.include_router(api_router)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'status_code': exc.status_code, 'status': exc.status, 'message': exc.message}
    )