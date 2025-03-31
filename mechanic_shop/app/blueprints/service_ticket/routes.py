@ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def update_ticket_mechanics(ticket_id):
    data = request.get_json()
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    if "add_ids" in data:
        for m_id in data["add_ids"]:
            mechanic = Mechanic.query.get(m_id)
            if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

    if "remove_ids" in data:
        for m_id in data["remove_ids"]:
            mechanic = Mechanic.query.get(m_id)
            if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.dump(ticket)