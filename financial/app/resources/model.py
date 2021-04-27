import collections
import typing

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from bson import ObjectId

from pydantic import BaseModel, Field

from app.conf import settings


class Invoice(BaseModel):
    """
    Base invoice model
    """
    appointment_id: str
    total_price: str

    class Config:
        """
        Encoders to avoid serialization errors
        on response
        """
        json_encoders = {ObjectId: lambda item: str(item)}

    @classmethod
    async def process_appointment(cls, data: dict) -> None:
        start_date = datetime.fromisoformat(data.get("start_date"))
        end_date = datetime.fromisoformat(data.get("end_date"))
        delta = end_date - start_date
        hours = (delta.seconds // 3600) or 1
        await cls.create({
            "appointment_id": data.get("id"),
            "total_price": hours * data.get("price")
        })


    @staticmethod
    async def create(data: dict) -> None:
        mongodb_client = AsyncIOMotorClient(settings.DB_URL)
        collection = mongodb_client[settings.DB_NAME]['invoice']
        await collection.insert_one(data)
        mongodb_client.close()


class InvoiceList(BaseModel):
    """
    Invoice list structure for pagination
    """
    page: typing.List[Invoice]
    page_size: int
    page_number: int
    count: int
