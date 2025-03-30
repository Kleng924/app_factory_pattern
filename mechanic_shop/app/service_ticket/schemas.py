from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import ServiceTicket  # adjust path to your models

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        fields = ('VIN', 'service_date', 'service_description', 'customer_id', 'mechanic_ids')