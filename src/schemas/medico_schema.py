# src/schemas/medico_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Medico

class MedicoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Medico
        load_instance = True

    Id = fields.Int()
    Nombre = fields.Str(required=True)
    Apellido = fields.Str(required=True)
    Telefono = fields.Str()
    Email = fields.Email()
    FechaBaja = fields.DateTime()
