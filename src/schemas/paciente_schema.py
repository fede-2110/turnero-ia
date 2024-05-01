# src/schemas/paciente_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchemaOpts
from src.model.db import db
from marshmallow import fields, validates, ValidationError
from src.model.models import Paciente
from datetime import datetime

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        sqla_session = db.session
        load_instance = True

    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    dni = fields.Str(required=True, validate=lambda x: x.isdigit())  
    fecha_nacimiento = fields.Date(required=True)
    telefono = fields.Str(required=False)
    email = fields.Email(required=False, allow_none=True)  
    fecha_baja = fields.DateTime(dump_only=True) 

    @validates('dni')
    def validate_dni(self, value):
            if len(value) > 6:
                raise ValidationError("El DNI debe tener al menos 6 dígitos.")
    
    @validates('fecha_nacimiento')
    def validate_fecha_nacimiento(self, value):
        if value >= datetime.today().date():
            raise ValidationError("La fecha de nacimiento debe ser anterior a la fecha actual.")