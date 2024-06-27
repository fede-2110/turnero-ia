from src.model.models import Servicio
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from injector import inject
from src.schemas.facturacion.servicio_schema import ServicioSchema

class ServicioService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow
        self.schema = ServicioSchema()

    def agregar_servicio(self, nuevo_servicio):
        self.schema.validate(nuevo_servicio)
        with self.uow.start():
            self.repo.add(nuevo_servicio)
            return nuevo_servicio

    def obtener_servicio_por_id(self, servicio_id):
        return self.repo.get_by_id(servicio_id)

    def actualizar_servicio(self, servicio_id, datos_actualizados):
        servicio = self.repo.get_by_id(servicio_id)
        self.schema.validate(datos_actualizados, partial=True)
        for key, value in datos_actualizados.items():
            setattr(servicio, key, value)
        with self.uow.start():
            return servicio

    def eliminar_servicio(self, servicio_id):
        servicio = self.repo.get_by_id(servicio_id)
        with self.uow.start():
            self.repo.delete(servicio)
