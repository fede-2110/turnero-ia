# src/service/centro_atencion_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import CentroAtencion
from src.utils.pagination import paginate

class CentroAtencionService:
    def __init__(self):
        self.repo = MysqlRepository(CentroAtencion)
        self.uow = UnitOfWork()

    def agregar_centro(self, nuevo_centro):
        with self.uow.start():
            self.repo.add(nuevo_centro)

    def obtener_centro_por_id(self, centro_id):
        return self.repo.get_by_id(centro_id)

    def obtener_centros(self):
        return self.repo.get_all()
    
    def obtener_centros_paginados(self, page, per_page, endpoint):
        return paginate(CentroAtencion.query, page, per_page, endpoint)

    def actualizar_centro(self, centro_actualizado):
        with self.uow.start():
            self.repo.update(centro_actualizado)

    def eliminar_centro(self, centro_id):
        centro_a_eliminar = self.obtener_centro_por_id(centro_id)
        if centro_a_eliminar:
            with self.uow.start():
                self.repo.delete(centro_a_eliminar)
