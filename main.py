from fastapi import FastAPI

from app import api
from app import tasks


app = FastAPI(title="Flow Manager Microservice")
app.include_router(api.router)
