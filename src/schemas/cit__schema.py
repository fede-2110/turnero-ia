# src/schemas/cita_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Cita

class CitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cita
        load_instance = True

    Id = fields.Int(dump_only=True)
    PacienteId = fields.Int(required=True)
    MedicoId = fields.Int(required=True)
    CentroId = fields.Int(required=True)
    ConsultorioId = fields.Int(allow_none=True)  # Permitir null para consultorios opcionales
    FechaHora = fields.DateTime(required=True)
    Estado = fields.Str(required=True)
    MotivoConsulta = fields.Str()
    FechaBaja = fields.DateTime()
