# src/service/cita_service.py
from src.repository.mysql_repository import MysqlRepository
from src.service.unit_of_work import UnitOfWork
from src.model.models import Cita
from src.utils.pagination import paginate
from datetime import timedelta, datetime
from src.service.practica_service import PracticaService
from src.service.horario_atencion_service import HorarioAtencionService
import json 

class CitaService:
    def __init__(self):
        self.repo = MysqlRepository(Cita)
        self.uow = UnitOfWork()
        self.practica_service = PracticaService()
        self.horario_atencion_service = HorarioAtencionService()
    
    def agregar_cita(self, nueva_cita):
        with self.uow.start():
            self.repo.add(nueva_cita)
            return nueva_cita

    def obtener_cita_por_id(self, cita_id):
        cita = self.repo.get_by_id(cita_id)
        if cita and cita.fecha_baja is None:
            return cita
        return None

    def obtener_citas(self, paciente_id=None):
        query = Cita.query.filter(Cita.fecha_baja == None)
        if paciente_id:
            query = query.filter(Cita.paciente_id == paciente_id)
        return query.all()
    
    def obtener_citas_paginadas(self, page, per_page, endpoint, paciente_id=None):
        query = Cita.query.filter(Cita.fecha_baja == None)
        if paciente_id:
            query = query.filter(Cita.paciente_id == paciente_id)
        return paginate(query, page, per_page, endpoint)

    def actualizar_cita(self, cita_id, datos_actualizados):
        cita_existente = self.obtener_cita_por_id(cita_id)
        if cita_existente:
            with self.uow.start():
                cita_existente.fecha_hora = datos_actualizados.get('fecha_hora', cita_existente.fecha_hora)
                cita_existente.estado = datos_actualizados.get('estado', cita_existente.estado)
                self.repo.update(cita_existente)
                return cita_existente
        return None

    def cancelar_cita(self, cita_id):
            cita_a_cancelar = self.obtener_cita_por_id(cita_id)
            if cita_a_cancelar:
                with self.uow.start():
                    cita_a_cancelar.estado = 'Cancelada'
                    cita_a_cancelar.fecha_baja = datetime.now()
                    self.repo.update(cita_a_cancelar)
                    return True
            return False
        
    def obtener_disponibilidad(self, medico_id, centro_id, practica_id, fecha_str):
        # Convertir la fecha de string a objeto datetime.date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        print(fecha)
        # Obtener el día de la semana
        dia_semana = fecha.weekday()  # Esto retorna 0 para lunes, 6 para domingo
        print(f"Fecha: {fecha}, Día de la semana: {dia_semana}")
        
            # Obtener duración de la práctica
        duracion = self.practica_service.obtener_duracion_por_id(practica_id)
        
        # Obtener horarios de atención
        horarios = self.horario_atencion_service.obtener_horarios_por_medico_y_centro(medico_id, centro_id)
        # Filtrar horarios por día específico
        horarios_del_dia = [h for h in horarios if h['dia_semana'] == dia_semana]

        # Calcular bloques de tiempo disponibles
        disponibles = []

        for horario in horarios_del_dia:
            inicio = datetime.combine(fecha, datetime.strptime(horario['hora_inicio'], '%H:%M:%S').time())
            fin = datetime.combine(fecha, datetime.strptime(horario['hora_fin'], '%H:%M:%S').time())
            while inicio + timedelta(minutes=duracion) <= fin:
                if self.es_tiempo_disponible(medico_id, centro_id, inicio, duracion):
                    disponibles.append(inicio.isoformat())
                inicio += timedelta(minutes=duracion)

        # Convertir la lista de fechas disponibles a formato JSON antes de devolverla
        return json.dumps(disponibles)
    
    def es_tiempo_disponible(self, medico_id, centro_id, inicio, duracion):
        print("Es tiempo disponible...")
        fin = inicio + timedelta(minutes=duracion)
        citas_existentes = Cita.query.filter(
            Cita.medico_id == medico_id,
            Cita.centro_id == centro_id,
            Cita.fecha_hora >= inicio,
            Cita.fecha_hora < fin,
            Cita.fecha_baja == None
        ).all()

        return len(citas_existentes) == 0
