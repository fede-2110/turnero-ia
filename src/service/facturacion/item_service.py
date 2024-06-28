from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.schemas.facturacion.item_schema import ItemSchema
from src.schemas.facturacion.precio_historico_schema import PrecioHistoricoSchema
from injector import inject
from datetime import date, datetime

class ItemService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork, item_schema: ItemSchema, precio_historico_schema: PrecioHistoricoSchema):
        self.repo = repo
        self.uow = uow
        self.item_schema = item_schema
        self.precio_historico_schema = precio_historico_schema

    def agregar_item(self, nuevo_item):
        print("Datos recibidos para agregar item:", nuevo_item)
        errores = self.item_schema.validate(nuevo_item)
        if errores:
            raise ValueError(errores)
        item = self.item_schema.load(nuevo_item)
        print("Item después de cargar el esquema:", item)
        with self.uow.start():
            self.repo.add(item)
        
        # Agregar precio histórico
        nuevo_precio = {
            'item_id': item.id,
            'precio': nuevo_item['precio'],
            'fecha_vigencia_inicio': date.today().isoformat(),
            'fecha_vigencia_fin': datetime(3000, 12, 31).date()
        }
        self.agregar_precio_historico(nuevo_precio)

        return self.item_schema.dump(item)

    def obtener_item_por_id(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            return None
        return self.item_schema.dump(item)

    def actualizar_item(self, item_id, datos_actualizados):
        print("Datos recibidos para actualizar item:", datos_actualizados)
        errores = self.item_schema.validate(datos_actualizados, partial=True)
        if errores:
            raise ValueError(errores)
        item = self.repo.get_by_id(item_id)
        if not item:
            return None
        for key, value in datos_actualizados.items():
            setattr(item, key, value)
        print("Item después de actualizar atributos:", item)
        with self.uow.start():
            self.repo.update(item)
        
        # Actualizar precio histórico
        if 'precio' in datos_actualizados:
            nuevo_precio = {
                'item_id': item.id,
                'precio': datos_actualizados['precio'],
                'fecha_vigencia_inicio': date.today().isoformat(),
                'fecha_vigencia_fin': datetime(3000, 12, 31).date()
            }
            self.agregar_precio_historico(nuevo_precio)

        return self.item_schema.dump(item)

    def agregar_precio_historico(self, nuevo_precio):
        errores = self.precio_historico_schema.validate(nuevo_precio)
        if errores:
            raise ValueError(errores)
        precio_historico = self.precio_historico_schema.load(nuevo_precio)
        print("Precio histórico después de cargar el esquema:", precio_historico)
        with self.uow.start():
            self.repo.add(precio_historico)
        return self.precio_historico_schema.dump(precio_historico)

    def eliminar_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            return None
        with self.uow.start():
            self.repo.delete(item)
        return True
