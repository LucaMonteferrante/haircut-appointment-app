from dataclasses import dataclass

@dataclass
class Appointment:
    id: int
    client_name: str
    phone_number: str
    appointment_date: str
    appointment_time: str
    barber_name: str
    service_type: str
    status: str = "Scheduled"
    notes: str = ""