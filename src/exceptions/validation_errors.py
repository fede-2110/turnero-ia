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
