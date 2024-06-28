from marshmallow import fields
from src.model.models import Item
from src.model.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        sqla_session = db.session
        load_instance = True
    
    id = auto_field(dump_only=True)
    nombre = auto_field(required=True)
    descripcion = auto_field()
    tipo_id = auto_field(required=True)
    precios_historicos = fields.List(fields.Nested('PrecioHistoricoSchema', exclude=('item',)))
