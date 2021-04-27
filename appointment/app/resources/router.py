from uuid import uuid4
from datetime import datetime

from fastapi import (
    APIRouter, Request, HTTPException, status,
)
from fastapi.encoders import jsonable_encoder

from app.resources.model import AppointmentBase, Appointment
from app.resources.producer import kafka_producer_instance
from app.conf import settings


router = APIRouter(tags=["appointment"])


@router.post(
    "/", response_description="Started appointment",
    response_model=Appointment
)
async def appointment_start(request: Request, appointment: AppointmentBase):
    """
    Edpoint to start/create an appointment

    Args:
        request (Request)
        appointment (AppointmentBase): appointment base data

    Returns:
        Appointment: appointment "complete" schema
    """
    database_instance = request.app.db['appointment']
    appointment_data = {
        **appointment.dict(),
        "start_date": datetime.now(),
        "id": str(uuid4()),
    }
    create_result = await database_instance.insert_one(
        jsonable_encoder(appointment_data)
    )
    return await database_instance.find_one(
        {"_id": create_result.inserted_id}
    )


@router.post(
    "/{id}", response_description="Started appointment",
    response_model=Appointment
)
async def appointment_end(request: Request, id: str):
    database_instance = request.app.db['appointment']

    update_result = await database_instance.update_one(
        {"id": id}, {"$set": {"end_date": datetime.now()}}
    )

    if not update_result.matched_count:
        raise HTTPException(
            detail="Appointment not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    appointment = await database_instance.find_one({"id": id})

    producer = kafka_producer_instance()
    producer.send(
        settings.KAFKA_TOPIC,
        jsonable_encoder(
            Appointment(**appointment).dict()
        )
    )

    return appointment

