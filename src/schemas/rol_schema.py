from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Rol

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True

    id = fields.Int()
    nombre = fields.Str(required=True)
    descripcion = fields.Str()