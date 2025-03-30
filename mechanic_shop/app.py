from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR MYSQL PASSWORD>@localhost/mechanic_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))

    cars = db.relationship('Car', backref='customer', lazy=True)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class Car(db.Model):
    __tablename__ = 'cars'

    car_id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    service_tickets = db.relationship('ServiceTicket', backref='car', lazy=True)

class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    mechanic_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    salary = db.Column(db.Float, nullable=False)

    service_assignments = db.relationship('ServiceAssignment', backref='mechanic', lazy=True)

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    ticket_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    service_assignments = db.relationship('ServiceAssignment', backref='service_ticket', lazy=True)

class ServiceAssignment(db.Model):
    __tablename__ = 'service_assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.ticket_id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.mechanic_id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

from app import db, Customer, Car, Mechanic, ServiceTicket, ServiceAssignment
from datetime import datetime

customer = Customer(first_name='John', last_name='Doe', phone_number='123-456-7890', email='john@example.com', address='123 Main St')
db.session.add(customer)
db.session.commit()

car = Car(vin='1HGCM82633A123456', make='Honda', model='Accord', year=2020, customer_id=customer.customer_id)
db.session.add(car)
db.session.commit()

mechanic = Mechanic(first_name='Mike', last_name='Smith', phone_number='123-555-7890', email='mike@example.com', address='456 Garage St', salary=45000)
db.session.add(mechanic)
db.session.commit()

service_ticket = ServiceTicket(car_id=car.car_id, service_date=datetime.utcnow(), description='Oil Change', total_cost=29.99)
db.session.add(service_ticket)
db.session.commit()

assignment = ServiceAssignment(ticket_id=service_ticket.ticket_id, mechanic_id=mechanic.mechanic_id)
db.session.add(assignment)
db.session.commit()

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data.get('phone_number'),
        email=data.get('email'),
        address=data.get('address')
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    return customers_schema.jsonify(all_customers)

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.phone_number = data.get('phone_number', customer.phone_number)
    customer.email = data.get('email', customer.email)
    customer.address = data.get('address', customer.address)
    
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

