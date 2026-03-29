import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
from model.appointment import Appointment

load_dotenv()


class MySqlAppointmentRepository:
    def __init__(
        self,
        host=None,
        port=None,
        user=None,
        password=None,
        database=None
    ):
        self._db_config = {
            "host": host or os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(port or os.getenv("DB_PORT", "3306")),
            "user": user or os.getenv("DB_USER", "root"),
            "password": password if password is not None else os.getenv("DB_PASSWORD", ""),
            "database": database or os.getenv("DB_NAME", "haircut_app"),
        }

        self._pool = pooling.MySQLConnectionPool(
            pool_name="haircut_pool",
            pool_size=5,
            **self._db_config
        )

        self._ensure_table()

    def _get_conn(self):
        return self._pool.get_connection()

    def _ensure_table(self):
        ddl = """
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            client_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            barber_name VARCHAR(100) NOT NULL,
            service_type VARCHAR(100) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Scheduled',
            notes TEXT
        )
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(ddl)
            conn.commit()
        finally:
            conn.close()

    def add(self, client_name, phone_number, appointment_date, appointment_time,
            barber_name, service_type, status="Scheduled", notes=""):
        sql = """
        INSERT INTO appointments
        (client_name, phone_number, appointment_date, appointment_time, barber_name, service_type, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (
                    client_name, phone_number, appointment_date, appointment_time,
                    barber_name, service_type, status, notes
                ))
                conn.commit()
                new_id = cur.lastrowid
                return Appointment(
                    id=new_id,
                    client_name=client_name,
                    phone_number=phone_number,
                    appointment_date=str(appointment_date),
                    appointment_time=str(appointment_time),
                    barber_name=barber_name,
                    service_type=service_type,
                    status=status,
                    notes=notes
                )
        finally:
            conn.close()

    def list_all(self):
        sql = """
        SELECT id, client_name, phone_number, appointment_date, appointment_time,
               barber_name, service_type, status, notes
        FROM appointments
        ORDER BY appointment_date, appointment_time, id
        """
        conn = self._get_conn()
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return [
                    Appointment(
                        id=row["id"],
                        client_name=row["client_name"],
                        phone_number=row["phone_number"],
                        appointment_date=str(row["appointment_date"]),
                        appointment_time=str(row["appointment_time"]),
                        barber_name=row["barber_name"],
                        service_type=row["service_type"],
                        status=row["status"],
                        notes=row["notes"] or ""
                    )
                    for row in rows
                ]
        finally:
            conn.close()

    def get_by_id(self, appointment_id):
        sql = """
        SELECT id, client_name, phone_number, appointment_date, appointment_time,
               barber_name, service_type, status, notes
        FROM appointments
        WHERE id = %s
        """
        conn = self._get_conn()
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql, (appointment_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return Appointment(
                    id=row["id"],
                    client_name=row["client_name"],
                    phone_number=row["phone_number"],
                    appointment_date=str(row["appointment_date"]),
                    appointment_time=str(row["appointment_time"]),
                    barber_name=row["barber_name"],
                    service_type=row["service_type"],
                    status=row["status"],
                    notes=row["notes"] or ""
                )
        finally:
            conn.close()

    def update(self, appointment_id, client_name, phone_number, appointment_date,
               appointment_time, barber_name, service_type, status, notes):
        sql = """
        UPDATE appointments
        SET client_name=%s, phone_number=%s, appointment_date=%s, appointment_time=%s,
            barber_name=%s, service_type=%s, status=%s, notes=%s
        WHERE id=%s
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (
                    client_name, phone_number, appointment_date, appointment_time,
                    barber_name, service_type, status, notes, appointment_id
                ))
                conn.commit()
                if cur.rowcount == 0:
                    return None
                return Appointment(
                    id=appointment_id,
                    client_name=client_name,
                    phone_number=phone_number,
                    appointment_date=str(appointment_date),
                    appointment_time=str(appointment_time),
                    barber_name=barber_name,
                    service_type=service_type,
                    status=status,
                    notes=notes
                )
        finally:
            conn.close()

    def delete(self, appointment_id):
        sql = "DELETE FROM appointments WHERE id = %s"
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (appointment_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()