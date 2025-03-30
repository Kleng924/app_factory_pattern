from . import ma
from .models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

class LoginSchema(ma.Schema):
    email = ma.String(required=True)
    password = ma.String(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()

class InventoryItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryItem
        load_instance = True

inventory_item_schema = InventoryItemSchema()
inventory_items_schema = InventoryItemSchema(many=True)