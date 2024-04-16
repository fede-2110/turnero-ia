# src/schemas/chat_schema.py
from marshmallow import Schema, fields, validate

class ChatSchema(Schema):
    message = fields.String(required=True, validate=validate.Length(min=1))
