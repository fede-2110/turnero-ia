# src/di/schema_module.py
from injector import Module, provider, singleton
from src.schemas.paciente_schema import PacienteSchema
from src.schemas.practica_schema import PracticaSchema
from src.schemas.cita_schema import CitaSchema
from src.schemas.medico_schema import MedicoSchema

class SchemaModule(Module):
    @provider
    @singleton
    def provide_paciente_schema(self) -> PacienteSchema:
        return PacienteSchema()
    
    @provider
    @singleton
    def provide_practica_schema(self) -> PracticaSchema:
        return PracticaSchema()
    
    @provider
    @singleton
    def provide_cita_schema(self) -> CitaSchema:
        return CitaSchema()
    
    @provider
    @singleton
    def provide_medico_schema(self) -> MedicoSchema:
        return MedicoSchema()
