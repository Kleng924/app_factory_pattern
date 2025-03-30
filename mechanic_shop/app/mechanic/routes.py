from flask import request, jsonify
from . import mechanic_bp
from .schemas import MechanicSchema
from app import db
from app.models import Mechanic

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    new_mechanic = mechanic_schema.load(data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    all_mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(all_mechanics)

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify(message="Mechanic deleted"), 204