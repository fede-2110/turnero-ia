from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import HorarioAtencion

class HorarioAtencionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HorarioAtencion
        load_instance = True

    id = fields.Int()
    medico_id = fields.Int(required=True)
    centro_id = fields.Int(required=True)
    dia_semana = fields.Int(required=True)
    hora_inicio = fields.Time(required=True)
    hora_fin = fields.Time(required=True)
    fecha_baja = fields.DateTime(dump_only=True)
