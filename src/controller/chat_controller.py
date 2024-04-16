# src/controller/chat_controller.py
from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.api_response import ApiResponse
from src.schemas.chat_schema import ChatSchema

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

chat_ns = Namespace('chat', description='Operaciones relacionadas con el chat')
chat_schema = ChatSchema()
chat_model = chat_ns.model('Chat', {
    'message': fields.String(required=True, description='Mensaje del usuario al chat')
})

client = OpenAI()
@chat_ns.route('/')
class Chat(Resource):
    @chat_ns.doc('post_chat')
    @chat_ns.expect(chat_model)
    def post(self):
        """Recibe la entrada del usuario y devuelve una respuesta generada por la IA"""
        data = request.get_json()
        errors = chat_schema.validate(data)
        if errors:
            return ApiResponse.client_error(message=str(errors), status=400)

        user_input = data['message']

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                    {"role": "user", "content": user_input}
                ]
            )
            chat_response = response.choices[0].message.content
            return ApiResponse.success(data={'message': chat_response})
        except Exception as e:
            if 'insufficient_quota' in str(e):
                return ApiResponse.server_error(message="Actualmente estamos experimentando un alto volumen de solicitudes. Por favor, intenta nuevamente en unos minutos.", status=429)
            return ApiResponse.server_error(message="Lo sentimos, estamos teniendo dificultades técnicas. Por favor, intenta nuevamente más tarde.")
