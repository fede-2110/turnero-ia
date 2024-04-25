# test_paciente_service.py
import pytest
from datetime import datetime
from src.service.paciente_service import PacienteService
from src.model.models import Paciente
from src.exceptions.validation_errors import ErrorDniDuplicado, ErrorPacienteNoActivo

def test_agregar_paciente_correctamente(session):
    """Verificar que se puede agregar un paciente correctamente."""
    service = PacienteService()
    nuevo_paciente = Paciente(nombre="John", apellido="Doe", dni="330001111", fecha_nacimiento=datetime(1990, 1, 1))
    paciente_agregado = service.agregar_paciente(nuevo_paciente)
    assert paciente_agregado is not None
    assert paciente_agregado.id is not None
    assert session.query(Paciente).filter_by(id=paciente_agregado.id).one_or_none() is not None

def test_agregar_paciente_con_dni_duplicado(session):
    """Verificar que la inserción falle si el DNI ya existe."""
    service = PacienteService()
    dni_compartido = "330001111"
    paciente1 = Paciente(nombre="John", apellido="Doe", dni=dni_compartido, fecha_nacimiento=datetime(1990, 1, 1))
    service.agregar_paciente(paciente1)  # Primera inserción debería ser exitosa

    # Intentar agregar otro paciente con el mismo DNI debería lanzar ErrorDniDuplicado
    paciente2 = Paciente(nombre="Jane", apellido="Doe", dni=dni_compartido, fecha_nacimiento=datetime(1995, 1, 1))
    with pytest.raises(ErrorDniDuplicado) as excinfo:
        service.agregar_paciente(paciente2)
    
    assert "Ya existe un paciente con el DNI 330001111" in str(excinfo.value)

def test_actualizar_paciente_inactivo(session):
    """Intenta actualizar un paciente que está inactivo (fecha_baja no es None)."""
    service = PacienteService()
    paciente = Paciente(nombre="Inactive", apellido="Patient", dni="330001112", fecha_nacimiento=datetime.now().date(), fecha_baja=datetime.now().date())
    session.add(paciente)
    session.commit()

    paciente_modificado = Paciente(nombre="Updated", apellido="Patient", dni="330001112", fecha_nacimiento=datetime.now().date())
    with pytest.raises(ErrorPacienteNoActivo):
        service.actualizar_paciente(paciente.id, paciente_modificado)

def test_eliminar_paciente_existente(session):
    """Verifica que se pueda marcar como eliminado (soft delete) un paciente existente."""
    service = PacienteService()
    paciente = Paciente(nombre="John", apellido="Doe", dni="330001113", fecha_nacimiento=datetime(1990, 1, 1))
    session.add(paciente)
    session.commit()
    
    # Confirmar que el paciente fue agregado y no tiene fecha de baja asignada
    assert paciente.fecha_baja is None
    
    # Ahora procedemos a marcar como eliminado al paciente
    service.eliminar_paciente(paciente.id)
    session.commit()
    
    # Verificar que el paciente ha sido marcado como eliminado
    paciente_eliminado = session.query(Paciente).filter_by(dni="330001113").first()
    assert paciente_eliminado.fecha_baja is not None

def test_obtener_paciente_por_id(session):
    """Verifica la recuperación de un paciente por su ID."""
    service = PacienteService()
    paciente = Paciente(nombre="John", apellido="Doe", dni="330001114", fecha_nacimiento=datetime(1990, 1, 1))
    session.add(paciente)
    session.commit()
    encontrado = service.obtener_paciente_por_id(paciente.id)
    assert encontrado is not None
    assert encontrado.id == paciente.id
