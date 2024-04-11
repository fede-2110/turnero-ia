# src/service/medico_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Medico
from src.utils.pagination import paginate

class MedicoService:
    def __init__(self):
        self.repo = MysqlRepository(Medico)
        self.uow = UnitOfWork()

    def agregar_medico(self, nuevo_medico):
        with self.uow.start():
            self.repo.add(nuevo_medico)

    def obtener_medico_por_id(self, medico_id):
        return self.repo.get_by_id(medico_id)

    def obtener_medicos(self):
        return self.repo.get_all()
    
    def obtener_medicos_paginados(self, page, per_page, endpoint):
        return paginate(Medico.query, page, per_page, endpoint)

    def actualizar_medico(self, medico_actualizado):
        with self.uow.start():
            self.repo.update(medico_actualizado)

    def eliminar_medico(self, medico_id):
        medico_a_eliminar = self.obtener_medico_por_id(medico_id)
        if medico_a_eliminar:
            with self.uow.start():
                self.repo.delete(medico_a_eliminar)