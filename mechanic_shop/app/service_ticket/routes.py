from flask import request, jsonify
from . import service_ticket_bp
from .schemas import ServiceTicketSchema
from app import db
from app.models import ServiceTicket, Mechanic

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    mechanic_ids = data.pop('mechanic_ids', [])
    ticket = ticket_schema.load(data)
    for mid in mechanic_ids:
        mechanic = Mechanic.query.get(mid)
        if mechanic:
            ticket.mechanics.append(mechanic)
    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201

@service_ticket_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(tickets)