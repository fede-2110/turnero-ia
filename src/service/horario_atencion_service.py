# src/service/horario_atencion_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import HorarioAtencion
from src.utils.pagination import paginate

class HorarioAtencionService:
    def __init__(self):
        self.repo = MysqlRepository(HorarioAtencion)
        self.uow = UnitOfWork()

    def agregar_horario_atencion(self, nuevo_horario_atencion):
        with self.uow.start():
            self.repo.add(nuevo_horario_atencion)

    def obtener_horario_atencion_por_id(self, horario_atencion_id):
        return self.repo.get_by_id(horario_atencion_id)

    def obtener_horarios_atencion(self):
        return self.repo.get_all()

    def obtener_horarios_paginados(self, page, per_page, endpoint):
        return paginate(HorarioAtencion.query, page, per_page, endpoint)
    
    def actualizar_horario_atencion(self, horario_atencion_actualizado):
        with self.uow.start():
            self.repo.update(horario_atencion_actualizado)

    # Asume que HorarioAtencion también implementa soft delete con FechaBaja
    def eliminar_horario_atencion(self, horario_atencion_id):
        horario_a_eliminar = self.obtener_horario_atencion_por_id(horario_atencion_id)
        if horario_a_eliminar:
            with self.uow.start():
                self.repo.delete(horario_a_eliminar)
