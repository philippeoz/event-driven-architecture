from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .conf import settings

from .resources.router import router


APP_SETTINGS = {
    "title": settings.APP_NAME,
    "version": settings.VERSION,
}


app = FastAPI(**APP_SETTINGS)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.db = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router)
