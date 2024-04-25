class ErrorValidacion(Exception):
    """Clase base para errores de validación."""
    pass

class ErrorDniDuplicado(ErrorValidacion):
    """Excepción para cuando se encuentra un DNI duplicado."""
    def __init__(self, dni):
        super().__init__(f"Ya existe un paciente con el DNI {dni}")

class ErrorPacienteNoActivo(ErrorValidacion):
    """Excepción para intentos de modificar o eliminar un paciente inactivo."""
    def __init__(self):
        super().__init__("El paciente está dado de baja y no se puede modificar o eliminar.")

class ErrorTelefonoDuplicado(ErrorValidacion):
    """Excepción para cuando se encuentra un teléfono duplicado en la base de datos."""
    def __init__(self, telefono):
        super().__init__(f"Ya existe un médico con el teléfono {telefono}")

class ErrorEmailDuplicado(ErrorValidacion):
    """Excepción para cuando se encuentra un email duplicado en la base de datos."""
    def __init__(self, email):
        super().__init__(f"Ya existe un médico con el email {email}")

class ErrorMedicoNoActivo(ErrorValidacion):
    """Excepción para intentos de modificar o eliminar un médico inactivo."""
    def __init__(self):
        super().__init__("El médico está dado de baja y no se puede modificar o eliminar.")
