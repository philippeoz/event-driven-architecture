import uvicorn

from app.conf import settings


if __name__ == "__main__":
    print(settings.HOST, settings.DEBUG_MODE, settings.PORT)
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
        log_level='info',
    )
