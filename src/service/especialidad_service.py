# src/service/especialidad_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Especialidad
from src.utils.pagination import paginate

class EspecialidadService:
    def __init__(self):
        self.repo = MysqlRepository(Especialidad)
        self.uow = UnitOfWork()

    def agregar_especialidad(self, nueva_especialidad):
        with self.uow.start():
            self.repo.add(nueva_especialidad)

    def obtener_especialidad_por_id(self, especialidad_id):
        return self.repo.get_by_id(especialidad_id)

    def obtener_especialidades(self):
        return self.repo.get_all()
    
    def obtener_especialidades_paginadas(self, page, per_page, endpoint):
        return paginate(Especialidad.query, page, per_page, endpoint)
    

    def actualizar_especialidad(self, especialidad_actualizada):
        with self.uow.start():
            self.repo.update(especialidad_actualizada)

    def eliminar_especialidad(self, especialidad_id):
        especialidad_a_eliminar = self.obtener_especialidad_por_id(especialidad_id)
        if especialidad_a_eliminar:
            with self.uow.start():
                self.repo.delete(especialidad_a_eliminar)
