# src/schemas/centro_atencion_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import CentroAtencion

class CentroAtencionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CentroAtencion
        load_instance = True

    Id = fields.Int()
    NombreCentro = fields.Str(required=True)
    Direccion = fields.Str(required=True)
    Telefono = fields.Str()
    FechaBaja = fields.DateTime()
