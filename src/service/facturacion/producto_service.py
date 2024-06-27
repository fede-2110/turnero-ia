from src.model.models import Producto
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from injector import inject
from src.schemas.facturacion.producto_schema import ProductoSchema

class ProductoService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow
        self.schema = ProductoSchema()

    def agregar_producto(self, nuevo_producto):
        self.schema.validate(nuevo_producto)
        with self.uow.start():
            self.repo.add(nuevo_producto)
            return nuevo_producto

    def obtener_producto_por_id(self, producto_id):
        return self.repo.get_by_id(producto_id)

    def actualizar_producto(self, producto_id, datos_actualizados):
        producto = self.repo.get_by_id(producto_id)
        self.schema.validate(datos_actualizados, partial=True)
        for key, value in datos_actualizados.items():
            setattr(producto, key, value)
        with self.uow.start():
            return producto

    def eliminar_producto(self, producto_id):
        producto = self.repo.get_by_id(producto_id)
        with self.uow.start():
            self.repo.delete(producto)
