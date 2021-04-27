import pytest

from app.resources.model import Invoice

APPOINTMENT_MOCK = {
    "physician_id": "string",
    "patient_id": "string",
    "id": "835b6280-4817-41a8-a498-2a7ac72e2058",
    "price": 200,
    "start_date": "2021-04-27T05:03:08.346138",
    "end_date": "2021-04-27T08:03:49.709000"
}

@pytest.mark.asyncio
async def test_process_appointment(test_app):
    Invoice.create = test_app.app.db['invoice'].create
    await Invoice.process_appointment(APPOINTMENT_MOCK)
    item = test_app.app.db['invoice'].db[0]
    assert item.get("appointment_id") == APPOINTMENT_MOCK.get("id")
    assert item.get("total_price") == 600


def test_invoice_retrieve(test_app):
    response = test_app.get(f'/{APPOINTMENT_MOCK.get("id")}')
    assert response.status_code == 200
    assert response.json() == {
        "appointment_id": APPOINTMENT_MOCK.get("id"),
        "total_price": '600',
    }
