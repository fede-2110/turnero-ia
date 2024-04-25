from src.exceptions.validation_errors import ErrorDniDuplicado, ErrorPacienteNoActivo, ErrorTelefonoDuplicado
from src.model.db import db
from src.model.models import Paciente
from src.model.models import Medico

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
def validar_datos_medico(medico, medico_id=None):
    """Valida los datos del médico antes de guardar en la base de datos."""
    if medico.telefono:
        query_telefono = db.session.query(Medico).filter(
            Medico.telefono == medico.telefono,
            Medico.fecha_baja == None
        )
        if medico_id:
            query_telefono = query_telefono.filter(Medico.id != medico_id)
        
        medico_existente_telefono = query_telefono.first()
        if medico_existente_telefono:
            raise ErrorTelefonoDuplicado(medico.telefono)

    if medico.email:
        query_email = db.session.query(Medico).filter(
            Medico.email == medico.email,
            Medico.fecha_baja == None
        )
        if medico_id:
            query_email = query_email.filter(Medico.id != medico_id)
        
        medico_existente_email = query_email.first()
        if medico_existente_email:
            raise ErrorTelefonoDuplicado(medico.email)

    if medico_id:
        medico_existente = db.session.query(Medico).filter_by(id=medico_id).first()
        if medico_existente and medico_existente.fecha_baja:
            raise ErrorMedicoNoActivo()

