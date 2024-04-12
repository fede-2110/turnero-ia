# src/controller/paciente_controller.py
from flask_restx import Namespace, Resource, fields
from flask import request
from src.service.paciente_service import PacienteService
from src.utils.api_response import ApiResponse
from src.schemas.paciente_schema import PacienteSchema

paciente_ns = Namespace('pacientes', description='Operaciones relacionadas con pacientes')
paciente_service = PacienteService()
paciente_schema = PacienteSchema()

paciente_model = paciente_ns.model('PacienteModel', {
    'nombre': fields.String(required=True, description='Nombre del paciente'),
    'apellido': fields.String(required=True, description='Apellido del paciente'),
    'dni': fields.String(required=True, description='DNI del paciente'),
})

@paciente_ns.route('/', endpoint='listar_pacientes')
class PacienteList(Resource):
    @paciente_ns.doc('list_pacientes')
    def get(self):
        """Obtiene todos los pacientes"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        result, meta = paciente_service.obtener_pacientes_paginados(page, per_page, paciente_schema,'listar_pacientes')
        return ApiResponse.success(data=result, meta={'pagination': meta})

    @paciente_ns.doc('create_paciente')
    @paciente_ns.expect(paciente_schema) 
    def post(self):
        """Agrega un paciente nuevo"""
        data = request.get_json()
        errors = paciente_schema.validate(data)
        if errors:
            return ApiResponse.client_error(message=str(errors), status=400)
        paciente = paciente_service.agregar_paciente(data)
        return ApiResponse.success(data=paciente_schema.dump(paciente), message="Paciente creado con éxito", status=201)

@paciente_ns.route('/<int:id>')
@paciente_ns.param('id', 'Identificador único del paciente')
class Paciente(Resource):
    @paciente_ns.doc('get_paciente')
    def get(self, id):
        """Obtener un paciente por su ID"""
        paciente = paciente_service.obtener_paciente_por_id(id)
        if paciente:
            return ApiResponse.success(data=paciente_schema.dump(paciente))
        else:
            return ApiResponse.client_error(message="Paciente no encontrado", status=404)

    @paciente_ns.doc('update_paciente')
    def put(self, id):
        """Actualizar un paciente existente"""
        data = request.get_json()
        errors = paciente_schema.validate(data)
        if errors:
            return ApiResponse.client_error(message=str(errors), status=400)
        paciente = paciente_service.actualizar_paciente(id, data)
        if paciente:
            return ApiResponse.success(data=paciente_schema.dump(paciente), message="Paciente actualizado con éxito")
        else:
            return ApiResponse.client_error(message="No se pudo actualizar el paciente", status=404)


    @paciente_ns.doc('delete_paciente')
    def delete(self, id):
        """Eliminar un paciente"""
        if paciente_service.eliminar_paciente(id):
            return ApiResponse.success(message="Paciente eliminado con éxito")
        else:
            return ApiResponse.failure(message="No se pudo eliminar el paciente", status=404)
