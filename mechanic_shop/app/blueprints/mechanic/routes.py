@mechanic_bp.route('/most-tickets', methods=['GET'])
def most_tickets():
    mechanics = Mechanic.query.outerjoin(Mechanic.service_tickets)\
        .group_by(Mechanic.id)\
        .order_by(db.func.count(ServiceTicket.id).desc())\
        .all()
    return mechanic_schema.dump(mechanics, many=True)