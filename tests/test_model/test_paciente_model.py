# test_paciente_model.py
import pytest
from datetime import datetime
from src.model.models import Paciente
from sqlalchemy.exc import IntegrityError

def test_create_paciente(session):
    """Test the creation of a patient."""
    fecha_nacimiento = datetime.strptime("1990-01-01", "%Y-%m-%d").date()  # Convertir la cadena a objeto date
    paciente = Paciente(nombre="John", apellido="Doe", dni="12345678", fecha_nacimiento=fecha_nacimiento)
    session.add(paciente)
    session.commit()

    # Act
    retrieved = session.query(Paciente).first()
    
    # Assert
    assert paciente.nombre == "John"
    assert paciente.apellido == "Doe"
    assert paciente.dni == "12345678"
    assert paciente.fecha_nacimiento == fecha_nacimiento
    assert paciente.telefono is None
    assert paciente.email is None
    assert paciente.fecha_baja is None

def test_update_existing_paciente(session):
    paciente = Paciente(nombre="Initial", apellido="Patient", dni="33999111", fecha_nacimiento=datetime.now().date())
    session.add(paciente)
    session.commit()

    # Act
    paciente.nombre = "Updated"
    session.commit()

    # Assert
    updated_paciente = session.query(Paciente).filter_by(dni="33999111").first()
    assert updated_paciente.nombre == "Updated"

def test_duplicate_dni_insertion(session):
    paciente1 = Paciente(nombre="John", apellido="Doe", dni="44444444", fecha_nacimiento=datetime.now().date())
    session.add(paciente1)
    session.commit()

    paciente2 = Paciente(nombre="Jane", apellido="Doe", dni="44444444", fecha_nacimiento=datetime.now().date())

    with pytest.raises(IntegrityError):
        session.add(paciente2)
        session.commit()

def test_delete_paciente(session):
    paciente = Paciente(nombre="John", apellido="Doe", dni="87654321", fecha_nacimiento=datetime.now().date())
    session.add(paciente)
    session.commit()

    session.delete(paciente)
    session.commit()

    deleted_paciente = session.query(Paciente).filter_by(dni="87654321").first()
    assert deleted_paciente is None

def test_insert_without_required_fields(session):
    paciente = Paciente()  # no fields set

    with pytest.raises(IntegrityError):
        session.add(paciente)
        session.commit()

