from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.api_response import ApiResponse
from src.schemas.chat_schema import ChatSchema
from src.service.paciente_service import PacienteService
from src.schemas.paciente_schema import PacienteSchema
from src.service.chat_service import ChatService
from src.service.thread_service import ThreadService
from injector import inject

chat_ns = Namespace('chat', description='Operaciones relacionadas con el chat')
chat_model = chat_ns.model('Chat', {
    'message': fields.String(required=True, description='Mensaje del usuario al chat')
})

class ChatController(Resource):
    @inject
    def __init__(self, chat_service: ChatService, thread_service: ThreadService, paciente_service: PacienteService, paciente_schema: PacienteSchema, chat_schema: ChatSchema):
        self.chat_service = chat_service
        self.thread_service = thread_service
        self.paciente_service = paciente_service
        self.paciente_schema = paciente_schema
        self.chat_schema = chat_schema
        super(ChatController, self).__init__()

@chat_ns.route('/create')
class ChatCreate(Resource):
    @inject
    def __init__(self, thread_service: ThreadService, *args, **kwargs):
        self.thread_service = thread_service
        super(ChatCreate, self).__init__(*args, **kwargs)

    @chat_ns.doc('create_chat')
    def post(self):
        """Inicia una nueva conversación con el asistente de IA"""
        try:
            thread = self.thread_service.create_thread()
            if thread:
                return ApiResponse.success(data={'thread_id': thread.id}, message="Thread creado con éxito.")
            else:
                return ApiResponse.client_error(message="No se pudo crear el thread.", status=400)
        except Exception as e:
            return ApiResponse.server_error(message=str(e))

@chat_ns.route('/update/<string:thread_id>')
@chat_ns.param('thread_id', 'El ID del thread de la conversación')
class ChatUpdate(Resource):
    @inject
    def __init__(self, chat_service: ChatService, thread_service: ThreadService, chat_schema: ChatSchema, *args, **kwargs):
        self.chat_service = chat_service
        self.thread_service = thread_service
        self.chat_schema = chat_schema
        super(ChatUpdate, self).__init__(*args, **kwargs)

    @chat_ns.doc('update_chat')
    @chat_ns.expect(chat_model)
    def post(self, thread_id):
        """Envía un mensaje al asistente en un thread existente y obtiene la respuesta"""
        data = request.get_json()
        errors = self.chat_schema.validate(data)
        if errors:
            return ApiResponse.client_error(message=str(errors), status=400)
        user_input = data['message']
        try:
            result = self.thread_service.process_message(thread_id, user_input)
            return ApiResponse.success(data={'message': result})
        except Exception as e:
            return ApiResponse.server_error(e)
