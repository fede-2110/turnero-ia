# src/controller/chat_controller.py
from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.api_response import ApiResponse
from src.schemas.chat_schema import ChatSchema
from openai import OpenAI
import os
import time

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

chat_ns = Namespace('chat', description='Operaciones relacionadas con el chat')
chat_schema = ChatSchema()
chat_model = chat_ns.model('Chat', {
    'message': fields.String(required=True, description='Mensaje del usuario al chat')
})

@chat_ns.route('/create')
class ChatCreate(Resource):
    @chat_ns.doc('create_chat')
    def post(self):
        """Inicia una nueva conversación con el asistente de IA"""
        try:
            # Crear un nuevo thread
            thread = client.beta.threads.create()

            # Faltaria persistirlo, proxima iteracion, evaluar si conviene.
            return ApiResponse.success(data={'thread_id': thread.id}, message="Thread iniciado con éxito.")
        except Exception as e:
            return ApiResponse.server_error(message=str(e))

@chat_ns.route('/update/<string:thread_id>')
@chat_ns.param('thread_id', 'El ID del thread de la conversación')
class ChatUpdate(Resource):
    @chat_ns.doc('update_chat')
    @chat_ns.expect(chat_model)  # Asegúrate de que el modelo de chat es adecuado para enviar mensajes
    def post(self, thread_id):
        """Envía un mensaje al asistente en un thread existente y obtiene la respuesta"""
        data = request.get_json()
        errors = chat_schema.validate(data)
        if errors:
            return ApiResponse.client_error(message=str(errors), status=400)

        user_input = data['message']
        try:
            # Añadir el mensaje del usuario al thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_input
            )
            # Ejecutar el asistente para procesar el mensaje y generar una respuesta
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=os.environ.get("ASSISTANT_ID")
            )
            # Esperar a que la ejecución del asistente complete
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
                time.sleep(1)
                
            # Obtener la última respuesta del asistente
            if run.status == "completed":
                message_response = client.beta.threads.messages.list(thread_id=thread_id)
                # Tomar el último mensaje generado por el asistente
                latest_message = message_response.data[0]  
                return ApiResponse.success(data={'message': latest_message.content[0].text.value})
            else:
                return ApiResponse.client_error(message="La solicitud no se completó correctamente.", status=424)
        except Exception as e:
            return ApiResponse.server_error(message=str(e))

