from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.model.models import Usuario
from werkzeug.security import generate_password_hash

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

    id = fields.Int()
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, load_only=True, deserialize='load_password')
    provider = fields.Str()
    provider_id = fields.Str()
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_baja = fields.DateTime()

    def load_password(self, value):
        return generate_password_hash(value)


