# src/di/repository_module.py
from injector import Module, provider
from src.repository.mysql_repository import MysqlRepository
from src.model.models import CentroAtencion, Paciente, Cita, Consultorio, HorarioAtencion, Practica, Especialidad, Medico

class RepositoryModule(Module):
    @provider
    def provide_centro_atencion_repository(self) -> MysqlRepository:
        return MysqlRepository(CentroAtencion)

    @provider
    def provide_paciente_repository(self) -> MysqlRepository:
        return MysqlRepository(Paciente)
    
    @provider
    def provide_cita_repository(self) -> MysqlRepository:
        return MysqlRepository(Cita)
    
    @provider
    def provide_horario_atencion_repository(self) -> MysqlRepository:
        return MysqlRepository(HorarioAtencion)
    
    @provider
    def provide_practica_repository(self) -> MysqlRepository:
        return MysqlRepository(Practica)
    
    @provider
    def provide_especialidad_repository(self) -> MysqlRepository:
        return MysqlRepository(Especialidad)
    
    @provider
    def provide_medico_repository(self) -> MysqlRepository:
        return MysqlRepository(Medico)
    
    @provider
    def provide_consultorio_repository(self) -> MysqlRepository:
        return MysqlRepository(Consultorio)
