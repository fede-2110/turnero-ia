# src/schemas/consultorio_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Consultorio

class ConsultorioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Consultorio
        load_instance = True  # Opcional: True si quieres que la deserialización cree instancias del modelo

    Id = fields.Int(dump_only=True)
    CentroId = fields.Int(required=True)
    NumeroConsultorio = fields.Str(required=True)
    FechaBaja = fields.DateTime()
