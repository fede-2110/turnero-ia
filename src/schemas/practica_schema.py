from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.model.models import Practica

class PracticaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Practica
        load_instance = True  # Optional: if True, makes the schema load a model instance

    id = auto_field(dump_only=True)
    nombre = auto_field(required=True)
    descripcion = auto_field(required=True)
    duracion_min = auto_field(required=True, validate=lambda x: x > 0)  # Validation to ensure duration is positive

