from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from model.mysql_repository import MySqlAppointmentRepository

appointment_bp = Blueprint("appointments", __name__)
repo = MySqlAppointmentRepository()

@appointment_bp.route("/")
def home():
    appointments = repo.list_all()
    return render_template("appointments.html", appointments=appointments)

@appointment_bp.route("/appointments/new", methods=["GET", "POST"])
def create_appointment():
    if request.method == "POST":
        repo.add(
            client_name=request.form["client_name"],
            phone_number=request.form["phone_number"],
            appointment_date=request.form["appointment_date"],
            appointment_time=request.form["appointment_time"],
            barber_name=request.form["barber_name"],
            service_type=request.form["service_type"],
            status=request.form["status"],
            notes=request.form["notes"]
        )
        return redirect(url_for("appointments.home"))

    return render_template("create_appointment.html")

@appointment_bp.route("/appointments/<int:appointment_id>/edit", methods=["GET", "POST"])
def edit_appointment(appointment_id):
    appointment = repo.get_by_id(appointment_id)
    if not appointment:
        return "Appointment not found", 404

    if request.method == "POST":
        repo.update(
            appointment_id=appointment_id,
            client_name=request.form["client_name"],
            phone_number=request.form["phone_number"],
            appointment_date=request.form["appointment_date"],
            appointment_time=request.form["appointment_time"],
            barber_name=request.form["barber_name"],
            service_type=request.form["service_type"],
            status=request.form["status"],
            notes=request.form["notes"]
        )
        return redirect(url_for("appointments.home"))

    return render_template("edit_appointment.html", appointment=appointment)

@appointment_bp.route("/appointments/<int:appointment_id>/delete", methods=["POST"])
def delete_appointment(appointment_id):
    repo.delete(appointment_id)
    return redirect(url_for("appointments.home"))

# API routes
@appointment_bp.route("/api/appointments", methods=["GET"])
def api_get_all():
    appointments = repo.list_all()
    return jsonify([a.__dict__ for a in appointments])

@appointment_bp.route("/api/appointments/<int:appointment_id>", methods=["GET"])
def api_get_one(appointment_id):
    appointment = repo.get_by_id(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment.__dict__)

@appointment_bp.route("/api/appointments", methods=["POST"])
def api_create():
    data = request.get_json()
    appointment = repo.add(
        client_name=data["client_name"],
        phone_number=data["phone_number"],
        appointment_date=data["appointment_date"],
        appointment_time=data["appointment_time"],
        barber_name=data["barber_name"],
        service_type=data["service_type"],
        status=data.get("status", "Scheduled"),
        notes=data.get("notes", "")
    )
    return jsonify(appointment.__dict__), 201

@appointment_bp.route("/api/appointments/<int:appointment_id>", methods=["PUT"])
def api_update(appointment_id):
    data = request.get_json()
    updated = repo.update(
        appointment_id=appointment_id,
        client_name=data["client_name"],
        phone_number=data["phone_number"],
        appointment_date=data["appointment_date"],
        appointment_time=data["appointment_time"],
        barber_name=data["barber_name"],
        service_type=data["service_type"],
        status=data["status"],
        notes=data.get("notes", "")
    )
    if not updated:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(updated.__dict__)

@appointment_bp.route("/api/appointments/<int:appointment_id>", methods=["DELETE"])
def api_delete(appointment_id):
    deleted = repo.delete(appointment_id)
    if not deleted:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify({"message": "Deleted successfully"})