from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import UsuarioRol

class UsuarioRolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioRol
        load_instance = True

    usuario_id = fields.Int(required=True)
    rol_id = fields.Int(required=True)