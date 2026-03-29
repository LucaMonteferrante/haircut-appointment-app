import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.mysql_repository import MySqlAppointmentRepository


TEST_DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Cucajay87",
    "database": "haircut_app_test",
}


def make_repo():
    return MySqlAppointmentRepository(**TEST_DB_CONFIG)


def clear_table(repo):
    conn = repo._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM appointments")
        conn.commit()
    finally:
        conn.close()


def test_add_appointment():
    repo = make_repo()
    clear_table(repo)

    appointment = repo.add(
        client_name="John Smith",
        phone_number="5145551234",
        appointment_date="2026-03-25",
        appointment_time="14:30:00",
        barber_name="Mike",
        service_type="Fade",
        status="Scheduled",
        notes="Test note"
    )

    assert appointment.id is not None
    assert appointment.client_name == "John Smith"
    assert appointment.barber_name == "Mike"
    assert appointment.service_type == "Fade"


def test_get_by_id():
    repo = make_repo()
    clear_table(repo)

    created = repo.add(
        client_name="Alice Brown",
        phone_number="1234567890",
        appointment_date="2026-03-26",
        appointment_time="10:00:00",
        barber_name="Sam",
        service_type="Trim"
    )

    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.client_name == "Alice Brown"


def test_list_all():
    repo = make_repo()
    clear_table(repo)

    repo.add(
        client_name="Client One",
        phone_number="1111111111",
        appointment_date="2026-03-27",
        appointment_time="09:00:00",
        barber_name="Alex",
        service_type="Buzz Cut"
    )

    repo.add(
        client_name="Client Two",
        phone_number="2222222222",
        appointment_date="2026-03-27",
        appointment_time="11:00:00",
        barber_name="Chris",
        service_type="Fade"
    )

    appointments = repo.list_all()

    assert len(appointments) == 2
    assert appointments[0].client_name is not None


def test_update_appointment():
    repo = make_repo()
    clear_table(repo)

    created = repo.add(
        client_name="Mark Lee",
        phone_number="3333333333",
        appointment_date="2026-03-28",
        appointment_time="13:00:00",
        barber_name="Jordan",
        service_type="Trim"
    )

    updated = repo.update(
        appointment_id=created.id,
        client_name="Mark Lee",
        phone_number="3333333333",
        appointment_date="2026-03-28",
        appointment_time="13:00:00",
        barber_name="Jordan",
        service_type="Trim",
        status="Completed",
        notes="Finished successfully"
    )

    assert updated is not None
    assert updated.status == "Completed"
    assert updated.notes == "Finished successfully"


def test_delete_appointment():
    repo = make_repo()
    clear_table(repo)

    created = repo.add(
        client_name="Delete Me",
        phone_number="4444444444",
        appointment_date="2026-03-29",
        appointment_time="15:00:00",
        barber_name="Taylor",
        service_type="Line Up"
    )

    result = repo.delete(created.id)
    fetched = repo.get_by_id(created.id)

    assert result is True
    assert fetched is None