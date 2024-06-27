from marshmallow import Schema, fields, validate, ValidationError

class ProductoSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    descripcion = fields.Str(validate=validate.Length(max=1000))
    precio = fields.Float(required=True, validate=lambda x: x > 0)
    fecha_vigencia_ini = fields.Date(required=True)
    fecha_vigencia_fin = fields.Date(required=True)
    
    def validate(self, data, partial=False):
        errors = super().validate(data, partial=partial)
        if data['fecha_vigencia_ini'] >= data['fecha_vigencia_fin']:
            errors['fecha_vigencia'] = ['La fecha de inicio debe ser anterior a la fecha de fin']
        if errors:
            raise ValidationError(errors)
