@ticket_bp.route('/<int:ticket_id>/add-part', methods=['POST'])
def add_part(ticket_id):
    data = request.get_json()
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get(data['inventory_id'])

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
    
    return service_ticket_schema.dump(ticket)