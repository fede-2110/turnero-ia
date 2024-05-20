# src/service/chat_service.py
from datetime import datetime
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

class ChatService:
    def __init__(self):
        self.paciente_service = PacienteService()
        self.paciente_schema = PacienteSchema()
        self.practica_schema = PracticaSchema()
        self.medico_schema = MedicoSchema()
        self.cita_schema = CitaSchema()
        self.centro_atencion_service = CentroAtencionService()
        self.horario_atencion_service = HorarioAtencionService()
        self.cita_service = CitaService()
        self.practica_service = PracticaService()
        self.especialidad_service = EspecialidadService()
        self.medico_service = MedicoService()

    def execute_function(self, function_name, arguments):
        if function_name == "fetch_patient_info":
            return self.fetch_patient_info(arguments)
        elif function_name == "create_patient":
            return self.create_patient(arguments)
        elif function_name == "get_centers_for_doctor":
            return self.get_centers_for_doctor(arguments)
        elif function_name == "get_available_days":
            return self.get_available_days(arguments)
        elif function_name == "get_appointment_availability":
            return self.get_appointment_availability(arguments)
        elif function_name == "fetch_practice_info":
            return self.fetch_practice_info(arguments)
        elif function_name == "fetch_specialty_id":
            return self.fetch_specialty_id(arguments)
        elif function_name == "fetch_doctors_by_specialty":
            return self.fetch_doctors_by_specialty(arguments)
        elif function_name == "fetch_current_day":
            return self.fetch_current_day()
        elif function_name == "create_appointment":
            return self.create_appointment(arguments)
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
        print(arguments)
        paciente = self.paciente_schema.load(arguments)
        nuevo_paciente = self.paciente_service.agregar_paciente(paciente)
        return self.paciente_schema.dump(nuevo_paciente)
    def get_latest_message(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id)
        return messages.data[0].content[0].text.value
    def get_centers_for_doctor(self, arguments):
        medico_id = arguments['medico_id']
        # TODO: a veces el id viene como otra cosa que un id
        print("id del medico: " + medico_id)
        #TODO: sacar el hardcore para la version grande.
        centers = self.centro_atencion_service.obtener_centros_por_medico(1)
        if centers:
            return centers
        else:
            return "No se encontraron centros para el médico especificado."
    def get_available_days(self, arguments): 
        #TODO: ver que siempre venga id de medico, ha venido p001 y doctora-pignatelli (ver si se arreglo con la funcion de obtener medico)
        #TODO: "EL ID DE LA DOCTORA ES X Y ANDUVO...  terrible!"
        print("id del medico: " + arguments['medico_id'])
        medico_id = 1
        centro_id = arguments['centro_id']
        print("El id del centro: " + centro_id)
        available_days = self.horario_atencion_service.obtener_horarios_por_medico_y_centro(medico_id, centro_id)
        if available_days:
            return available_days
        else:
            return "No hay días disponibles para las citas en el centro seleccionado."
    def get_appointment_availability(self, arguments):
        medico_id = arguments['medico_id']
        print("id del medico: " + medico_id)
        centro_id = arguments['centro_id']
        fecha_solicitada = arguments['date']
        print("La fecha solicitada: " + fecha_solicitada)
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
        print ("especialidad a buscar: " + descripcion)
        specialty = self.especialidad_service.obtener_especialidad_por_descripcion(descripcion)
        if specialty:
            return specialty.id
        else:
            return "Especialidad no encontrada"
    def fetch_doctors_by_specialty(self, arguments):
        medico_id = arguments['specialty_id']
        print("id del medico: " + medico_id)
        medicos = self.medico_service.obtener_medicos_por_especialidad(medico_id)
        if medicos:
            return self.medico_schema.dump(medicos, many=True)
        else:
            return "Especialidad no encontrada"
    def fetch_practice_info(self, arguments):
        practice_description = arguments['practice_description']
        especialidad_id = arguments.get('specialty_id', None)
        print("practica: " + practice_description)
        print("especialidad: " + especialidad_id)
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
    @staticmethod
    def fetch_current_day():
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        day_of_week = (current_datetime.weekday() + 1) % 7
        print("El día del sistema: " + current_date)
        print("Día de la semana: " + str(day_of_week))
        return {
            "current_date": current_date,
            "day_of_week": day_of_week
        }