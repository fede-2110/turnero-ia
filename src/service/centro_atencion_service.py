# src/service/centro_atencion_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import CentroAtencion
from src.utils.pagination import paginate
from src.model.models import MedicoCentro
from src.schemas.centro_atencion_schema import CentroAtencionSchema
from src.model.db import db
from injector import inject

class CentroAtencionService:
    @inject
    def __init__(self, repo: MysqlRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

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

    def obtener_centros_por_medico(self, medico_id):
    # Consulta para obtener centros en los que un médico específico trabaja
        consulta = db.session.query(CentroAtencion).join(MedicoCentro).filter(
        MedicoCentro.medico_id == medico_id,
        CentroAtencion.fecha_baja == None,
        )
        centros = consulta.all()
        centro_schema = CentroAtencionSchema(many=True)
        return centro_schema.dump(centros)
        
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
