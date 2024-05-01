# src/service/medico_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Medico
from src.utils.pagination import paginate
from src.model.db import db
from src.model.models import MedicoEspecialidad

class MedicoService:
    def __init__(self):
        self.repo = MysqlRepository(Medico)
        self.uow = UnitOfWork()

    def agregar_medico(self, nuevo_medico):
        with self.uow.start():
            self.repo.add(nuevo_medico)
            return nuevo_medico

    def obtener_medico_por_id(self, medico_id):
        return self.repo.get_by_id(medico_id)

    def obtener_medicos(self):
        return self.repo.get_all()

    def obtener_medicos_por_especialidad(self, especialidad_id):
        # Realiza la consulta para obtener médicos que están en una especialidad específica
        medicos = db.session.query(Medico).join(MedicoEspecialidad, Medico.id == MedicoEspecialidad.medico_id).filter(
            MedicoEspecialidad.especialidad_id == especialidad_id,
            Medico.fecha_baja == None
        ).all()
        # Utiliza el esquema para serializar la lista de objetos de médicos
        return medicos
    
    def obtener_medicos_paginados(self, page, per_page, schema, endpoint):
        return paginate(Medico.query, page=page, per_page=per_page, schema=schema, endpoint=endpoint)
    
    def actualizar_medico(self, medico_id, medico_actualizado):
        medico_existente = self.repo.get_by_id(medico_id)
        if medico_existente:
            with self.uow.start():
                medico_existente.nombre = medico_actualizado.get('nombre', medico_existente.nombre)
                medico_existente.apellido = medico_actualizado.get('apellido', medico_existente.apellido)
                medico_existente.telefono = medico_actualizado.get('telefono', medico_existente.telefono)
                medico_existente.email = medico_actualizado.get('email', medico_existente.email)
                self.repo.update(medico_existente)
                return medico_existente
        return None

    def eliminar_medico(self, medico_id):
        medico_a_eliminar = self.obtener_medico_por_id(medico_id)
        # TODO: validaciones que el medico no tenga turnos tomados

        if medico_a_eliminar:
            with self.uow.start():
                self.repo.delete(medico_a_eliminar)
                return True
        return False
