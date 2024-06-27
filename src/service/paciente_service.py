# src/service/paciente_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Paciente
from src.utils.pagination import paginate
from src.model.db import db
from src.utils.validation_utils import validar_datos_paciente
from src.utils.cleanup_utils import clean_dni
from injector import inject

class PacienteService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    def agregar_paciente(self, nuevo_paciente):
        validar_datos_paciente(nuevo_paciente)
        with self.uow.start():
            self.repo.add(nuevo_paciente)
            return nuevo_paciente

    def obtener_paciente_por_id(self, paciente_id):
        # No se necesita UoW ya que es solo una operación de lectura
        paciente = self.repo.get_by_id(paciente_id)
        if paciente and paciente.fecha_baja is None:
            return paciente
        return None
    
    def obtener_pacientes(self):
        # Igual que arriba, solo lectura
        return self.repo.get_all()

    def obtener_pacientes_paginados(self, page, per_page, schema, endpoint):
        return paginate(Paciente.query, page=page, per_page=per_page, schema=schema, endpoint=endpoint)
    
    def actualizar_paciente(self, paciente_id, paciente_actualizado):
        validar_datos_paciente(paciente_actualizado, paciente_id)
        paciente_existente = self.repo.get_by_id(paciente_id)
        if paciente_existente:
            with self.uow.start():
                if paciente_actualizado.dni is not None:
                    paciente_existente.dni = paciente_actualizado.dni
                if paciente_actualizado.nombre is not None:
                    paciente_existente.nombre = paciente_actualizado.nombre
                if paciente_actualizado.apellido is not None:
                    paciente_existente.appellido = paciente_actualizado.apellido
                if paciente_actualizado.fecha_nacimiento is not None:
                    paciente_existente.fecha_nacimiento = paciente_actualizado.fecha_nacimiento
                if paciente_actualizado.telefono is not None:
                    paciente_existente.telefono = paciente_actualizado.telefono
                if paciente_actualizado.email is not None:
                    paciente_existente.email = paciente_actualizado.email    
                
                self.repo.update(paciente_existente)
                return paciente_existente
        return None
        

    def eliminar_paciente(self, paciente_id):
        paciente_a_eliminar = self.obtener_paciente_por_id(paciente_id)
        # TODO: validaciones que el paciente no tenga turnos tomados
        if paciente_a_eliminar:
            with self.uow.start():
                self.repo.delete(paciente_a_eliminar)
                return True
        return False 
    
    def obtener_paciente_por_dni(self, parametros):
        dni = clean_dni(parametros)
        consulta = db.session.query(Paciente).filter(Paciente.fecha_baja == None, Paciente.dni == dni)
        return consulta.first()