from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import api_router
from exception import UnicornException

app = FastAPI(title='API Eco River')


app.include_router(api_router)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'status_code': exc.status_code, 'status': exc.status, 'message': exc.message}
    )