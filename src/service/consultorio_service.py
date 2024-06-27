# src/service/consultorio_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Consultorio
from src.utils.pagination import paginate
from injector import inject
class ConsultorioService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    def agregar_consultorio(self, nuevo_consultorio):
        with self.uow.start():
            self.repo.add(nuevo_consultorio)
            return nuevo_consultorio

    def obtener_consultorio_por_id(self, consultorio_id):
        consultorio = self.repo.get_by_id(consultorio_id)
        if consultorio and consultorio.fecha_baja is None:
            return consultorio
        return None

    def obtener__consultorios(self):
        return self.repo.get_all()

    def obtener_consultorios_paginados(self, page, per_page, endpoint):
        return paginate(Consultorio.query.filter(Consultorio.fecha_baja == None), page, per_page, endpoint)


    def actualizar_consultorio(self, consultorio_actualizado):
        with self.uow.start():
            self.repo.update(consultorio_actualizado)

    # Asume que Consultorio también implementa soft delete con FechaBaja
    def eliminar_consultorio(self, consultorio_id):
        consultorio_a_eliminar = self.obtener_consultorio_por_id(consultorio_id)
        if consultorio_a_eliminar:
            with self.uow.start():
                self.repo.delete(consultorio_a_eliminar)
                return consultorio_a_eliminar
        return None