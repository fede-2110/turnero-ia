# src/di/service_module.py
from injector import Module, provider, singleton
from src.service.unit_of_work import UnitOfWork
from src.service.paciente_service import PacienteService
from src.service.consultorio_service import ConsultorioService
from src.service.centro_atencion_service import CentroAtencionService
from src.service.cita_service import CitaService
from src.service.horario_atencion_service import HorarioAtencionService
from src.service.practica_service import PracticaService
from src.service.especialidad_service import EspecialidadService
from src.service.medico_service import MedicoService
from src.service.chat_service import ChatService
from src.service.thread_service import ThreadService
from src.repository.mysql_repository import MysqlRepository
from src.schemas.cita_schema import CitaSchema
from src.schemas.paciente_schema import PacienteSchema
from src.schemas.practica_schema import PracticaSchema
from src.schemas.facturacion.item_schema import ItemSchema
from src.schemas.medico_schema import MedicoSchema
from src.service.facturacion.factura_service import FacturaService
from src.service.facturacion.item_service import ItemService
from src.service.facturacion.afip_service import AFIPService
import os
from pyafipws.wsaa import WSAA

class ServiceModule(Module):
    @provider
    def provide_unit_of_work(self) -> UnitOfWork:
        return UnitOfWork()
    
    @provider
    def provide_centro_atencion_service(self, repo: MysqlRepository, uow: UnitOfWork) -> CentroAtencionService:
        return CentroAtencionService(repo, uow)
    
    @provider
    def provide_paciente_service(self, repo: MysqlRepository, uow: UnitOfWork) -> PacienteService:
        return PacienteService(repo, uow)
    
    @provider
    def provide_cita_service(self, repo: MysqlRepository, uow: UnitOfWork, practica_service: PracticaService, horario_atencion_service: HorarioAtencionService) -> CitaService:
        return CitaService(repo, uow, practica_service, horario_atencion_service)

    @provider
    def provide_horario_atencion_service(self, repo: MysqlRepository, uow: UnitOfWork) -> HorarioAtencionService:
        return HorarioAtencionService(repo, uow)
    
    @provider
    def provide_practica_service(self, repo: MysqlRepository, uow: UnitOfWork) -> PracticaService:
        return PracticaService(repo, uow)
    
    @provider
    def provide_especialidad_service(self, repo: MysqlRepository, uow: UnitOfWork) -> EspecialidadService:
        return EspecialidadService(repo, uow)
    
    @provider
    def provide_medico_service(self, repo: MysqlRepository, uow: UnitOfWork) -> MedicoService:
        return MedicoService(repo, uow)
    
    @provider
    def provide_consultorio_service(self, repo: MysqlRepository, uow: UnitOfWork) -> ConsultorioService:
        return ConsultorioService(repo, uow)
    
    @provider
    @singleton
    def provide_chat_service(self, 
                             paciente_service: PacienteService,
                             centro_atencion_service: CentroAtencionService,
                             cita_service: CitaService,
                             horario_atencion_service: HorarioAtencionService,
                             practica_service: PracticaService,
                             especialidad_service: EspecialidadService,
                             medico_service: MedicoService,
                             paciente_schema: PacienteSchema,
                             practica_schema: PracticaSchema,
                             medico_schema: MedicoSchema,
                             cita_schema: CitaSchema) -> ChatService:
        return ChatService(paciente_service, 
                           centro_atencion_service, 
                           cita_service, 
                           horario_atencion_service, 
                           practica_service, 
                           especialidad_service, 
                           medico_service, 
                           paciente_schema, 
                           practica_schema, 
                           medico_schema, 
                           cita_schema)
    
    @provider
    @singleton
    def provide_thread_service(self, chat_service: ChatService) -> ThreadService:
        return ThreadService(chat_service)
    @provider
    def provide_producto_service(self, repo: MysqlRepository, uow: UnitOfWork, schema: ItemSchema) -> ItemService:
        return ItemService(repo, uow, schema)

    @provider
    @singleton
    def provide_factura_service(self, factura_repo: MysqlRepository, detalle_repo: MysqlRepository, uow: UnitOfWork) -> FacturaService:
        return FacturaService(factura_repo, detalle_repo, uow)
    
    @singleton
    @provider
    def provide_wsaa(self) -> WSAA:
        return WSAA()
    
    @singleton
    @provider
    def provide_afip_service(self) -> AFIPService:
        # Proporcionar los valores necesarios para inicializar AFIPService
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cert_path = os.path.join(base_dir, 'certs', 'cert.crt')
        key_path = os.path.join(base_dir, 'certs', 'private.key')
        cuit = '27-36086640-3'
        return AFIPService(cuit, cert_path, key_path)