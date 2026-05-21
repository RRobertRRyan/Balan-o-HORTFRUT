from flask import Flask
from app.models.models import init_db
from app.routes.routes import main_bp, api_bp


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = "hortfrut-villefort-2024"

    init_db()

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
