# src/schemas/paciente_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.model.models import Paciente

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        load_instance = True
