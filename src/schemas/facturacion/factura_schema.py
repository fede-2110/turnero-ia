from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class FacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    paciente_id = fields.Int(required=True)
    fecha_emision = fields.DateTime(dump_only=True)
    cae = fields.Str(required=True, validate=validate.Length(equal=14))  # assuming CAE is 14 characters
    fecha_vencimiento_cae = fields.Date(required=True)
    total = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0.01))

    @validates('fecha_vencimiento_cae')
    def validate_fecha_vencimiento_cae(self, value):
        if value < datetime.today().date():
            raise ValidationError('La fecha de vencimiento del CAE debe ser una fecha futura.')
