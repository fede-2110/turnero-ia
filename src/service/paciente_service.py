# src/service/paciente_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Paciente
from src.utils.pagination import paginate

class PacienteService:
    def __init__(self):
        self.repo = MysqlRepository(Paciente)
        self.uow = UnitOfWork()

    def agregar_paciente(self, nuevo_paciente):
        with self.uow.start():
            self.repo.add(nuevo_paciente)

    def obtener_paciente_por_id(self, paciente_id):
        # No se necesita UoW ya que es solo una operación de lectura
        return self.repo.get_by_id(paciente_id)

    def obtener_pacientes(self):
        # Igual que arriba, solo lectura
        return self.repo.get_all()

    def obtener_pacientes_paginados(self, page, per_page, schema, endpoint):
        return paginate(Paciente.query, page=page, per_page=per_page, schema=schema, endpoint=endpoint)
    
    def actualizar_paciente(self, paciente_actualizado):
        with self.uow.start():
            self.repo.update(paciente_actualizado)

    def eliminar_paciente(self, paciente_id):
        paciente_a_eliminar = self.obtener_paciente_por_id(paciente_id)
        if paciente_a_eliminar:
            with self.uow.start():
                self.repo.delete(paciente_a_eliminar)
