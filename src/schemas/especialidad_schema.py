from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Especialidad

class EspecialidadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Especialidad
        load_instance = True

    id = fields.Int(dump_only=True)
    nombre_especialidad = fields.String(required=True)
    descripcion = fields.String(required=False)