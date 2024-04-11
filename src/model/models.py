# src/model/models.py
from src.model.db import db

class Paciente(db.Model):
    __tablename__ = 'Pacientes'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellido = db.Column(db.String(255), nullable=False)
    DNI = db.Column(db.String(20), unique=True, nullable=False)
    FechaDeNacimiento = db.Column(db.Date, nullable=False)
    Telefono = db.Column(db.String(20))
    Email = db.Column(db.String(255))
    FechaBaja = db.Column(db.DateTime)

class Medico(db.Model):
    __tablename__ = 'Medicos'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellido = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.String(20))
    Email = db.Column(db.String(255))
    FechaBaja = db.Column(db.DateTime)

class Especialidad(db.Model):
    __tablename__ = 'Especialidades'
    
    Id = db.Column(db.Integer, primary_key=True)
    NombreEspecialidad = db.Column(db.String(255), nullable=False)
    Descripcion = db.Column(db.Text)
    FechaBaja = db.Column(db.DateTime)

class CentroAtencion(db.Model):
    __tablename__ = 'CentrosAtencion'
    
    Id = db.Column(db.Integer, primary_key=True)
    NombreCentro = db.Column(db.String(255), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.String(20))
    FechaBaja = db.Column(db.DateTime)

class Consultorio(db.Model):
    __tablename__ = 'Consultorios'
    
    Id = db.Column(db.Integer, primary_key=True)
    CentroId = db.Column(db.Integer, db.ForeignKey('CentrosAtencion.Id'), nullable=False)
    NumeroConsultorio = db.Column(db.String(50))
    FechaBaja = db.Column(db.DateTime)

class Cita(db.Model):
    __tablename__ = 'Citas'
    
    Id = db.Column(db.Integer, primary_key=True)
    PacienteId = db.Column(db.Integer, db.ForeignKey('Pacientes.Id'), nullable=False)
    MedicoId = db.Column(db.Integer, db.ForeignKey('Medicos.Id'), nullable=False)
    CentroId = db.Column(db.Integer, db.ForeignKey('CentrosAtencion.Id'), nullable=False)
    ConsultorioId = db.Column(db.Integer, db.ForeignKey('Consultorios.Id'), nullable=True)
    FechaHora = db.Column(db.DateTime, nullable=False)
    Estado = db.Column(db.String(50))
    MotivoConsulta = db.Column(db.Text)
    FechaBaja = db.Column(db.DateTime)

class MedicoEspecialidad(db.Model):
    __tablename__ = 'MedicosEspecialidades'
    
    MedicoId = db.Column(db.Integer, db.ForeignKey('Medicos.Id'), primary_key=True)
    EspecialidadId = db.Column(db.Integer, db.ForeignKey('Especialidades.Id'), primary_key=True)

class MedicoCentro(db.Model):
    __tablename__ = 'MedicosCentros'
    
    MedicoId = db.Column(db.Integer, db.ForeignKey('Medicos.Id'), primary_key=True)
    CentroId = db.Column(db.Integer, db.ForeignKey('CentrosAtencion.Id'), primary_key=True)

class HorarioAtencion(db.Model):
    __tablename__ = 'HorariosAtencion'
    
    Id = db.Column(db.Integer, primary_key=True)
    MedicoId = db.Column(db.Integer, db.ForeignKey('Medicos.Id'), nullable=False)
    CentroId = db.Column(db.Integer, db.ForeignKey('CentrosAtencion.Id'), nullable=False)
    DiaSemana = db.Column(db.String(10), nullable=False)
    HoraInicio = db.Column(db.Time, nullable=False)
    HoraFin = db.Column(db.Time, nullable=False)
    FechaBaja = db.Column(db.DateTime)
