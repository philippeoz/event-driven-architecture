from datetime import datetime

from fastapi import (
    APIRouter, Request, HTTPException, status,
)
from fastapi.encoders import jsonable_encoder

from app.resources.model import Invoice
from app.conf import settings


router = APIRouter(tags=["invoices"])


@router.get(
    "/{appointment_id}", response_description="Started appointment",
    response_model=Invoice
)
async def invoice_detail(request: Request, appointment_id: str):
    """
    Endpoint do get invoice details

    Args:
        request (Request)
        appointment_id (str)

    Returns:
        Invoice: invoice schema
    """
    database_instance = request.app.db['invoice']
    return await database_instance.find_one(
        {"appointment_id": appointment_id}
    )
