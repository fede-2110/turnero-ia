# src/model/models.py
from .db import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(255))
    fecha_baja = db.Column(db.DateTime)

class Medico(db.Model):
    __tablename__ = 'medico'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(255))
    fecha_baja = db.Column(db.DateTime)

class Especialidad(db.Model):
    __tablename__ = 'especialidad'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_especialidad = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_baja = db.Column(db.DateTime)

class CentroAtencion(db.Model):
    __tablename__ = 'centro_atencion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_centro = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_baja = db.Column(db.DateTime)

class Consultorio(db.Model):
    __tablename__ = 'consultorio'
    
    id = db.Column(db.Integer, primary_key=True)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro_atencion.id'), nullable=False)
    numero_consultorio = db.Column(db.String(50))
    fecha_baja = db.Column(db.DateTime)

class Cita(db.Model):
    __tablename__ = 'cita'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro_atencion.id'), nullable=False)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorio.id'), nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50))
    motivo_consulta = db.Column(db.Text)
    fecha_baja = db.Column(db.DateTime)

class MedicoEspecialidad(db.Model):
    __tablename__ = 'medico_especialidad'
    
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), primary_key=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), primary_key=True)

class MedicoCentro(db.Model):
    __tablename__ = 'medico_centro'
    
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), primary_key=True)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro_atencion.id'), primary_key=True)

class HorarioAtencion(db.Model):
    __tablename__ = 'horario_atencion'
    
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro_atencion.id'), nullable=False)
    dia_semana = db.Column(db.String(10), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    fecha_baja = db.Column(db.DateTime)
