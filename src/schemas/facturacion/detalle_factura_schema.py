from marshmallow import Schema, fields, validate, validates, ValidationError

class DetalleFacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    factura_id = fields.Int(required=True)
    tipo = fields.Str(required=True)
    producto_id = fields.Int(allow_none=True)
    servicio_id = fields.Int(allow_none=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))
    precio_unitario = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0.01))
    subtotal = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0.01))

    @validates('subtotal')
    def validate_subtotal(self, value, **kwargs):
        cantidad = self.context.get('cantidad')
        precio_unitario = self.context.get('precio_unitario')
        if cantidad and precio_unitario and value != cantidad * precio_unitario:
            raise ValidationError('El subtotal debe ser igual a cantidad * precio_unitario.')

    @validates('producto_id')
    def validate_producto_id(self, value, **kwargs):
        if value is None and self.context.get('servicio_id') is None:
            raise ValidationError('Debe proporcionar al menos un producto_id o un servicio_id.')

    @validates('servicio_id')
    def validate_servicio_id(self, value, **kwargs):
        if value is None and self.context.get('producto_id') is None:
            raise ValidationError('Debe proporcionar al menos un producto_id o un servicio_id.')
