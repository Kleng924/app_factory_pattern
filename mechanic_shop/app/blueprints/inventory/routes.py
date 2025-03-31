@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    parts = Inventory.query.all()
    return inventory_schema.dump(parts, many=True)

@inventory_bp.route('/', methods=['POST'])
def create_part():
    data = request.get_json()
    part = inventory_schema.load(data)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.dump(part), 201

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return inventory_schema.dump(part)

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return {"message": "Deleted"}