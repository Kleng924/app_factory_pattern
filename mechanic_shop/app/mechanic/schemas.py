from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic  # adjust path to your models

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True