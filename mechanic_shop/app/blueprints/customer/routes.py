from app.auth.utils import encode_token
from app.auth.decorators import token_required
from .schemas import login_schema

@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    validated = login_schema.load(data)
    customer = db.session.query(Customer).filter_by(email=validated['email']).first()

    if not customer or not customer.verify_password(validated['password']):
        return {"message": "Invalid credentials"}, 401
    
    token = encode_token(customer.id)
    return {"token": token}

@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_ticket_schema.dump(tickets, many=True)

@customer_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Customer.query.paginate(page=page, per_page=per_page)
    return {
        "total": pagination.total,
        "pages": pagination.pages,
        "data": customer_schema.dump(pagination.items, many=True)
    }