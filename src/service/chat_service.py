# src/service/chat_service.py
from datetime import datetime
from injector import inject
from src.service.paciente_service import PacienteService
from src.service.centro_atencion_service import CentroAtencionService
from src.service.cita_service import CitaService
from src.schemas.paciente_schema import PacienteSchema
from src.schemas.practica_schema import PracticaSchema
from src.schemas.cita_schema import CitaSchema
from src.schemas.medico_schema import MedicoSchema
from src.service.horario_atencion_service import HorarioAtencionService
from src.service.practica_service import PracticaService
from src.service.especialidad_service import EspecialidadService
from src.service.medico_service import MedicoService
import json

class ChatService:
    @inject
    def __init__(self, 
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
                 cita_schema: CitaSchema):
        self.paciente_service = paciente_service
        self.paciente_schema = paciente_schema
        self.practica_schema = practica_schema
        self.medico_schema = medico_schema
        self.cita_schema = cita_schema
        self.centro_atencion_service = centro_atencion_service
        self.horario_atencion_service = horario_atencion_service
        self.cita_service = cita_service
        self.practica_service = practica_service
        self.especialidad_service = especialidad_service
        self.medico_service = medico_service
        self.current_day_info = None
        
    def execute_function(self, function_name, arguments):
        print(f"{function_name}: {json.dumps(arguments, indent=2)}")
        
        function_map = {
            "fetch_patient_info": self.fetch_patient_info,
            "create_patient": self.create_patient,
            "get_centers_for_doctor": self.get_centers_for_doctor,
            "get_available_days": self.get_available_days,
            "get_appointment_availability": self.get_appointment_availability,
            "fetch_practice_info": self.fetch_practice_info,
            "fetch_specialty_id": self.fetch_specialty_id,
            "fetch_doctors_by_specialty": self.fetch_doctors_by_specialty,
            "fetch_current_day": self.fetch_current_day,
            "create_appointment": self.create_appointment
        }
        if function_name in function_map:
            if not arguments:
                return function_map[function_name]()
            else:
                return function_map[function_name](arguments)
        return "Function not handled"

    def fetch_patient_info(self, arguments):
        dni = arguments['patient_dni']
        paciente = self.paciente_service.obtener_paciente_por_dni(dni)
        if paciente:
            paciente_info = self.paciente_schema.dump(paciente)
            return paciente_info
        else:
            return "Paciente no encontrado"
    def create_patient(self, arguments):
        paciente = self.paciente_schema.load(arguments)
        nuevo_paciente = self.paciente_service.agregar_paciente(paciente)
        return self.paciente_schema.dump(nuevo_paciente)

    def get_centers_for_doctor(self, arguments):
        medico_id = arguments['medico_id']
        # TODO: a veces el id viene como otra cosa que un id
        #TODO: sacar el hardcore para la version grande.
        centers = self.centro_atencion_service.obtener_centros_por_medico(1)
        if centers:
            return centers
        else:
            return "No se encontraron centros para el médico especificado."
    def get_available_days(self, arguments): 
        #TODO: ver que siempre venga id de medico, ha venido p001 y doctora-pignatelli (ver si se arreglo con la funcion de obtener medico)
        #TODO: "EL ID DE LA DOCTORA ES X Y ANDUVO...  terrible!"
        medico_id = 1
        centro_id = arguments['centro_id']
        available_days = self.horario_atencion_service.obtener_horarios_por_medico_y_centro(medico_id, centro_id)
        if available_days:
            return available_days
        else:
            return "No hay días disponibles para las citas en el centro seleccionado."
    def get_appointment_availability(self, arguments):
        medico_id = arguments['medico_id']
        centro_id = arguments['centro_id']
        fecha_solicitada = arguments['date']
        practica_id = arguments['practica_id']
        # Este método debería comunicarse con un servicio que gestione las citas para verificar disponibilidad.
        centro = self.centro_atencion_service.obtener_centro_por_id(centro_id)
        if centro.es_por_orden_de_llegada:
            return "Este centro opera por orden de llegada. No es necesario reservar turno. Puede presentarse directamente."
        else:
            # Realiza la lógica para consultar la disponibilidad de turnos
            horarios_disponibles = self.cita_service.obtener_disponibilidad(medico_id,centro_id,practica_id,fecha_solicitada)
            if horarios_disponibles:
                return horarios_disponibles
            else:
                return "No hay turnos disponibles para la fecha seleccionada."
    def fetch_specialty_id(self, arguments):
        descripcion = arguments['specialty_description']
        specialty = self.especialidad_service.obtener_especialidad_por_descripcion(descripcion)
        if specialty:
            return specialty.id
        else:
            return "Especialidad no encontrada"
    def fetch_doctors_by_specialty(self, arguments):
        medico_id = arguments['specialty_id']
        medicos = self.medico_service.obtener_medicos_por_especialidad(medico_id)
        if medicos:
            return self.medico_schema.dump(medicos, many=True)
        else:
            return "Especialidad no encontrada"
    def fetch_practice_info(self, arguments):
        practice_description = arguments['practice_description']
        especialidad_id = arguments.get('specialty_id', None)
        practices = self.practica_service.obtener_practicas_por_descripcion_y_especialidad(
            practice_description, especialidad_id)
        
        if practices:
            # Suponiendo que quieras devolver todas las prácticas encontradas
            return self.practica_schema.dump(practices, many=True)
        else:
            return "Práctica no encontrada"
    def create_appointment(self, arguments):
        cita = self.cita_schema.load(arguments)
        nueva_cita = self.cita_service.agregar_cita(cita)
        return self.cita_schema.dump(nueva_cita)
    
    # @staticmethod
    # def fetch_current_day():
    #     current_datetime = datetime.now()
    #     current_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    #     day_of_week = (current_datetime.weekday() + 1) % 7
    #     print("El día del sistema: " + current_date)
    #     print("Día de la semana: " + str(day_of_week))
    #     return {
    #         "current_date": current_date,
    #         "day_of_week": day_of_week
    #     }
    
    @staticmethod
    def fetch_current_day():
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        day_of_week = current_datetime.weekday()
        print("El día del sistema: " + current_date)
        print("Día de la semana: " + str(day_of_week))
        return {
            "current_date": current_date,
            "day_of_week": day_of_week
        }
