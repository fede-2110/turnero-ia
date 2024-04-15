from src.exceptions.validation_errors import ErrorDniDuplicado, ErrorPacienteNoActivo
from src.model.db import db
from src.model.models import Paciente

def validar_datos_paciente(paciente, paciente_id=None):
    """Valida los datos del paciente antes de guardar en la base de datos."""
    query = db.session.query(Paciente).filter(
        Paciente.dni == paciente.dni,
        Paciente.fecha_baja == None
    )
    if paciente_id:
        query = query.filter(Paciente.id != paciente_id)
    
    existente = query.first()
    if existente:
        raise ErrorDniDuplicado(paciente.dni)

    if paciente_id and not paciente.fecha_baja:
        paciente_existente = db.session.query(Paciente).filter_by(id=paciente_id).first()
        if paciente_existente and paciente_existente.fecha_baja:
            raise ErrorPacienteNoActivo()
