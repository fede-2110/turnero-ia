from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.model.models import PrecioHistorico
from src.model.db import db

class PrecioHistoricoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PrecioHistorico
        sqla_session = db.session
        load_instance = True
    
    id = auto_field(dump_only=True)
    item_id = auto_field(required=True)
    precio = auto_field(required=True)
    fecha_vigencia_inicio = auto_field(required=True)
    fecha_vigencia_fin = auto_field(required=True)
