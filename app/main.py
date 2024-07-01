from fastapi import FastAPI
from routers import api_router

app = FastAPI(title="API Eco River")


app.include_router(api_router)

