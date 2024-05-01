from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.model.models import Cita

class CitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cita
        load_instance = True  # Optional: if True, makes the schema load a model instance

    id = auto_field(dump_only=True)
    paciente_id = auto_field(required=True)
    medico_id = auto_field(required=True)
    centro_id = auto_field(required=True)
    consultorio_id = auto_field()  # Opcional
    fecha_hora = auto_field(required=True)
    estado = auto_field(required=True)
    id_practica = auto_field(required=True)