# src/service/horario_atencion_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import HorarioAtencion
from src.schemas.horario_atencion_schema import HorarioAtencionSchema
from src.utils.pagination import paginate

class HorarioAtencionService:
    def __init__(self):
        self.repo = MysqlRepository(HorarioAtencion)
        self.uow = UnitOfWork()

    def agregar_horario_atencion(self, nuevo_horario_atencion):
        with self.uow.start():
            self.repo.add(nuevo_horario_atencion)
            return nuevo_horario_atencion

    def obtener_horarios_por_medico_y_centro(self, medico_id, centro_id):
        horarios = HorarioAtencion.query.filter(
            HorarioAtencion.medico_id == medico_id,
            HorarioAtencion.centro_id == centro_id,
            HorarioAtencion.fecha_baja == None
        ).all()
        horario_schema = HorarioAtencionSchema(many=True)
        return horario_schema.dump(horarios)

    
    def obtener_horario_atencion_por_id(self, horario_atencion_id):
        return self.repo.get_by_id(horario_atencion_id)
    
    def obtener_horarios_paginados(self, page, per_page, endpoint):
        return paginate(HorarioAtencion.query, page, per_page, endpoint)
    
    def actualizar_horario_atencion(self, horario_id, datos_horario):
        horario_existente = self.repo.get_by_id(horario_id)
        if horario_existente and horario_existente.fecha_baja is None:
            with self.uow.start():
                horario_existente.dia_semana = datos_horario.get('dia_semana', horario_existente.dia_semana)
                horario_existente.hora_inicio = datos_horario.get('hora_inicio', horario_existente.hora_inicio)
                horario_existente.hora_fin = datos_horario.get('hora_fin', horario_existente.hora_fin)
                self.repo.update(horario_existente)
                return horario_existente
        return None
    
    # Asume que HorarioAtencion también implementa soft delete con FechaBaja
    def eliminar_horario_atencion(self, horario_atencion_id):
        horario_a_eliminar = self.obtener_horario_atencion_por_id(horario_atencion_id)
        if horario_a_eliminar:
            with self.uow.start():
                self.repo.delete(horario_a_eliminar)
                return True
        return False 