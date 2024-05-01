from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Practica
from src.model.models import Especialidad
from src.model.db import db

class PracticaService:
    def __init__(self):
        self.repo = MysqlRepository(Practica)
        self.uow = UnitOfWork()

    def agregar_practica(self, nueva_practica):
        with self.uow.start():
            self.repo.add(nueva_practica)
            return nueva_practica

    def obtener_practica_por_id(self, practica_id):
        practica = self.repo.get_by_id(practica_id)
        if practica and practica.fecha_baja is None:
            return practica
        return None

    def obtener_practicas_por_descripcion_y_especialidad(self, description, especialidad_id=None):
        query = db.session.query(Practica)
        if especialidad_id:
            query = query.join(Especialidad).filter(Especialidad.id == especialidad_id)
            practicas = query.filter(Practica.descripcion.ilike(f"%{description}%")).all()
            return practicas

    def actualizar_practica(self, practica_id, datos_actualizados):
        practica_existente = self.obtener_practica_por_id(practica_id)
        if practica_existente:
            with self.uow.start():
                practica_existente.nombre = datos_actualizados.get('nombre', practica_existente.nombre)
                practica_existente.descripcion = datos_actualizados.get('descripcion', practica_existente.descripcion)
                practica_existente.duracion_min = datos_actualizados.get('duracion', practica_existente.duracion_min)
                self.repo.update(practica_existente)
                return practica_existente
        return None

    def obtener_duracion_por_id(self, practica_id):
        practica = self.obtener_practica_por_id(practica_id)
        if practica:
            return practica.duracion_min
        return None
