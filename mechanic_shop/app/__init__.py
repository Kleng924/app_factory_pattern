from flask import Flask
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    return app