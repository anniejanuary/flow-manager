from fastapi import FastAPI

from app import api
from app.utils.logger import setup_logging


setup_logging()

app = FastAPI(title="Flow Manager Microservice")
app.include_router(api.router)
