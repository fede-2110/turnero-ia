# src/service/especialidad_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Especialidad
from src.model.db import db
from src.utils.pagination import paginate

class EspecialidadService:
    def __init__(self):
        self.repo = MysqlRepository(Especialidad)
        self.uow = UnitOfWork()

    def agregar_especialidad(self, nueva_especialidad):
        with self.uow.start():
            self.repo.add(nueva_especialidad)
            return nueva_especialidad

    def obtener_especialidad_por_id(self, especialidad_id):
        especialidad = self.repo.get_by_id(especialidad_id)
        if especialidad and especialidad.fecha_baja is None:
            return especialidad
        return None

    def obtener_especialidad_por_descripcion(self, description):
        return db.session.query(Especialidad).filter(Especialidad.nombre_especialidad.ilike(f"%{description}%")).first()

    def obtener_especialidades(self):
        return self.repo.get_all()
    
    def obtener_especialidades_paginadas(self, page, per_page, endpoint):
        return paginate(Especialidad.query.filter(Especialidad.fecha_baja == None), page, per_page, endpoint)
    
    def actualizar_especialidad(self, especialidad_actualizada):
        with self.uow.start():
            self.repo.update(especialidad_actualizada)

    def eliminar_especialidad(self, especialidad_id):
        especialidad_a_eliminar = self.obtener_especialidad_por_id(especialidad_id)
        if especialidad_a_eliminar:
            with self.uow.start():
                self.repo.delete(especialidad_a_eliminar)
                return especialidad_a_eliminar
        return None