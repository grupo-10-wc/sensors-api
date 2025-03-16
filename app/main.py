from app.sensor import models
from app.sensor import controller as sensor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine
import asyncio


app = FastAPI()

@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sensor.router, prefix='/api/sensors')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
