# src/service/cita_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Cita
from src.utils.pagination import paginate

class CitaService:
    def __init__(self):
        self.repo = MysqlRepository(Cita)
        self.uow = UnitOfWork()

    def agregar_cita(self, nueva_cita):
        with self.uow.start():
            self.repo.add(nueva_cita)

    def obtener_cita_por_id(self, cita_id):
        return self.repo.get_by_id(cita_id)

    def obtener_citas(self):
        return self.repo.get_all()
    
    def obtener_citas_paginadas(self, page, per_page, endpoint):
        return paginate(Cita.query, page, per_page, endpoint)
    

    def actualizar_cita(self, cita_actualizada):
        with self.uow.start():
            self.repo.update(cita_actualizada)

    def eliminar_cita(self, cita_id):
        cita_a_eliminar = self.obtener_cita_por_id(cita_id)
        if cita_a_eliminar:
            with self.uow.start():
                self.repo.delete(cita_a_eliminar)
