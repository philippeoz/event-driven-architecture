import uuid
import typing

from datetime import datetime

from bson import ObjectId

from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    """
    Base appointment model with required data only
    """
    physician_id: str
    patient_id: str


class Appointment(AppointmentBase):
    """Appointment Base Model"""
    id: str = Field(default_factory=uuid.uuid4)
    price: float = Field(default=200.00)
    start_date: datetime
    end_date: datetime = None

    class Config:
        """
        Encoders to avoid serialization errors
        on response
        """
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda item: str(item)}


class AppointmentList(BaseModel):
    """
    Appointment list structure for pagination
    """
    page: typing.List[Appointment]
    page_size: int
    page_number: int
    count: int
