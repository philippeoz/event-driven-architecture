import json


def test_appointment_start(test_app):
    response = test_app.post('/', data=json.dumps(
        {
            "physician_id": "12345",
            "patient_id": "12345666",
        }
    ))
    data = response.json()
    assert response.status_code == 200
    assert data.get("start_date") is not None
    assert data.get("end_date") is None


def test_appointment_end(test_app):
    appointment = test_app.post('/', data=json.dumps(
        {
            "physician_id": "12345",
            "patient_id": "12345666",
        }
    )).json()
    appointment_id = appointment.get("id")
    response = test_app.post(f'/{appointment_id}')
    data = response.json()
    assert response.status_code == 200
    assert data.get("start_date") is not None
    assert data.get("end_date") is not None
