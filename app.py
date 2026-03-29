from flask import Flask
from controller.appointment_controller import appointment_bp

app = Flask(
    __name__,
    template_folder="view/templates",
    static_folder="view/static"
)

app.register_blueprint(appointment_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)