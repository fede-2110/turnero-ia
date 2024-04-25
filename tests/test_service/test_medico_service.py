# test_medico_service.py
import pytest
from datetime import datetime
from src.service.medico_service import MedicoService
from src.model.models import Medico
from src.exceptions.validation_errors import ErrorTelefonoDuplicado, ErrorMedicoNoActivo

def test_agregar_medico_correctamente(session):
    """Verificar que se puede agregar un médico correctamente."""
    service = MedicoService()
    nuevo_medico = Medico(nombre="John", apellido="Smith", telefono="123456789", email="john.smith@example.com")
    medico_agregado = service.agregar_medico(nuevo_medico)
    assert medico_agregado is not None
    assert medico_agregado.id is not None
    assert session.query(Medico).filter_by(id=medico_agregado.id).one_or_none() is not None

def test_eliminar_medico_existente(session):
    """Verifica que se pueda marcar como eliminado (soft delete) un médico existente."""
    service = MedicoService()
    medico = Medico(nombre="John", apellido="Smith", telefono="123456791", email="delete@example.com")
    session.add(medico)
    session.commit()
    
    # Confirmar que el médico fue agregado y no tiene fecha de baja asignada
    assert medico.fecha_baja is None
    
    # Ahora procedemos a marcar como eliminado al médico
    service.eliminar_medico(medico.id)
    session.commit()
    
    # Verificar que el médico ha sido marcado como eliminado
    medico_eliminado = session.query(Medico).filter_by(telefono="123456791").first()
    assert medico_eliminado.fecha_baja is not None

def test_obtener_medico_por_id(session):
    """Verifica la recuperación de un médico por su ID."""
    service = MedicoService()
    medico = Medico(nombre="John", apellido="Doe", telefono="123456792", email="john.doe@example.com")
    session.add(medico)
    session.commit()
    encontrado = service.obtener_medico_por_id(medico.id)
    assert encontrado is not None
    assert encontrado.id == medico.id
