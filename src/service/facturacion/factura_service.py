from src.model.models import Factura, DetalleFactura
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from injector import inject
from src.schemas.facturacion.factura_schema import FacturaSchema
from src.schemas.facturacion.detalle_factura_schema import DetalleFacturaSchema
from marshmallow import ValidationError

class FacturaService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow
        self.factura_schema = FacturaSchema()
        self.detalle_factura_schema = DetalleFacturaSchema()

    def agregar_factura(self, nueva_factura):
        try:
            self.factura_schema.load(nueva_factura)
            for detalle in nueva_factura['detalles']:
                self.detalle_factura_schema.load(detalle)

            factura = self.factura_schema.load(nueva_factura)
            detalles = [self.detalle_factura_schema.load(detalle) for detalle in nueva_factura['detalles']]
            factura.detalles = detalles

            with self.uow.start():
                self.repo.add(factura)
                return self.factura_schema.dump(factura)
        except ValidationError as e:
            raise e

    def obtener_factura_por_id(self, factura_id):
        factura = self.repo.get_by_id(factura_id)
        if factura:
            return self.factura_schema.dump(factura)
        return None

    def actualizar_factura(self, factura_id, datos_actualizados):
        factura = self.repo.get_by_id(factura_id)
        try:
            self.factura_schema.load(datos_actualizados, partial=True)

            for key, value in datos_actualizados.items():
                if key == 'detalles':
                    factura.detalles = [self.detalle_factura_schema.load(detalle) for detalle in value]
                else:
                    setattr(factura, key, value)

            with self.uow.start():
                return self.factura_schema.dump(factura)
        except ValidationError as e:
            raise e

    def eliminar_factura(self, factura_id):
        factura = self.repo.get_by_id(factura_id)
        with self.uow.start():
            self.repo.delete(factura)
