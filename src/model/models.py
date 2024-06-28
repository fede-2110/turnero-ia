# src/model/models.py
from .db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    
class Practica(db.Model):
    __tablename__ = 'practica'
    id = db.Column(db.Integer, primary_key=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_min = db.Column(db.Integer, nullable=False)
    fecha_baja = db.Column(db.DateTime)
    
class CentroAtencion(db.Model):
    __tablename__ = 'centro_atencion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_centro = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    es_por_orden_de_llegada = db.Column(db.Boolean, default=False, nullable=False)
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
    practica_id = db.Column(db.Integer, db.ForeignKey('practica.id'), nullable=False)
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
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    fecha_baja = db.Column(db.DateTime)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(50))
    provider_id = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_baja = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Rol(db.Model):
    __tablename__ = 'rol'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)

class UsuarioRol(db.Model):
    __tablename__ = 'usuario_rol'
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), primary_key=True)
    usuario = db.relationship('Usuario', back_populates='roles')
    rol = db.relationship('Rol', back_populates='usuarios')

Usuario.roles = db.relationship('UsuarioRol', back_populates='usuario')
Rol.usuarios = db.relationship('UsuarioRol', back_populates='rol')

# Tablas para Facturación

class TipoItem(db.Model):
    __tablename__ = 'tipo_item'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    items = db.relationship('Item', back_populates='tipo')

class Item(db.Model):
    __tablename__ = 'item'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_item.id'), nullable=False)
    tipo = db.relationship('TipoItem', back_populates='items')
    precios_historicos = db.relationship('PrecioHistorico', back_populates='item')

class PrecioHistorico(db.Model):
    __tablename__ = 'precio_historico'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_vigencia_inicio = db.Column(db.Date, nullable=False)
    fecha_vigencia_fin = db.Column(db.Date, nullable=False, default=datetime(3000, 12, 31).date())
    
    item = db.relationship('Item', back_populates='precios_historicos')

class Factura(db.Model):
    __tablename__ = 'factura'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    tipo = db.Column(db.String(50))
    cae = db.Column(db.String(50))
    fecha_vencimiento_cae = db.Column(db.Date)
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)