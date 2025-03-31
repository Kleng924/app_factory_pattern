from flask import Flask
from .models import db
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from .limiter_and_cache import limiter, cache  # if using external limiter/cache init

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') 

    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    Migrate(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    from .blueprints.customer import customer_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import ticket_bp
    from .blueprints.inventory import inventory_bp

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(ticket_bp, url_prefix='/tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app

from app import limiter, cache

limiter = Limiter(get_remote_address, default_limits=["100 per day", "10 per minute"])

@customer_bp.route("/limited")
@limiter.limit("5 per minute")  
def limited():
    return {"message": "This route is rate-limited"}

@customer_bp.route("/cached")
@cache.cached(timeout=60)  
def cached():
    return {"data": "This is cached for 60 seconds"}