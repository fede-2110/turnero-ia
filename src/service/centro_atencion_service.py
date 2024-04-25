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
            return nuevo_centro

    def obtener_centro_por_id(self, centro_id):
        centro = self.repo.get_by_id(centro_id)
        if centro and centro.fecha_baja is None:
            return centro
        return None

    def obtener_centros(self):
        return self.repo.get_all()
    
    def obtener_centros_paginados(self, page, per_page, endpoint):
        return paginate(CentroAtencion.query.filter(CentroAtencion.fecha_baja == None), page, per_page, endpoint)

    def actualizar_centro(self, centro_id, centro_actualizado):
        centro_existente = self.obtener_centro_por_id(centro_id)
        if centro_existente:
            with self.uow.start():
                centro_existente.nombre_centro = centro_actualizado.get('nombre_centro', centro_existente.nombre_centro)
                centro_existente.direccion = centro_actualizado.get('direccion', centro_existente.direccion)
                centro_existente.telefono = centro_actualizado.get('telefono', centro_existente.telefono)
                self.repo.update(centro_existente)
                return centro_existente
        return None

    def eliminar_centro(self, centro_id):
        centro_a_eliminar = self.obtener_centro_por_id(centro_id)
        if centro_a_eliminar:
            with self.uow.start():
                self.repo.update(centro_a_eliminar)
                return True
        return False
