from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class WorkLog(db.Model):
    __tablename__ = 'work_logs'
    
    work_log_id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.mechanic_id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.ticket_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    task_type = db.Column(db.String(100))
    hours_billed = db.Column(db.Float)

    mechanic = db.relationship('Mechanic', backref='work_logs')
    ticket = db.relationship('ServiceTicket', backref='work_logs')

class TicketPartUsage(db.Model):
    __tablename__ = 'ticket_part_usages'
    
    usage_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.ticket_id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.part_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_per_part = db.Column(db.Float, nullable=False)
    install_date = db.Column(db.Date)

    ticket = db.relationship('ServiceTicket', backref='part_usages')
    part = db.relationship('Part', backref='part_usages')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    appointment_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.mechanic_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50))
    estimated_duration = db.Column(db.Float)

    customer = db.relationship('Customer', backref='appointments')
    mechanic = db.relationship('Mechanic', backref='appointments')

class PerformanceLog(db.Model):
    __tablename__ = 'performance_logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.mechanic_id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.ticket_id'), nullable=False)
    time_taken = db.Column(db.Float)
    customer_feedback = db.Column(db.String(255))
    rating = db.Column(db.Integer)

    mechanic = db.relationship('Mechanic', backref='performance_logs')
    ticket = db.relationship('ServiceTicket', backref='performance_logs')

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(100))

    def __repr__(self):
        return f'<Item {self.name} ({self.quantity} in stock)>'

from . import db

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(100))
