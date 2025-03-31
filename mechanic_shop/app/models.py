ticket_inventory = db.Table(
    'ticket_inventory',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id')),
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_ticket.id'))
)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    tickets = db.relationship("ServiceTicket", secondary=ticket_inventory, back_populates="parts")

class ServiceTicket(db.Model):
    ...
    parts = db.relationship("Inventory", secondary=ticket_inventory, back_populates="tickets")