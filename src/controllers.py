# src/controller.py
from src.controller.paciente_controller import paciente_ns

#Registro de namespeaces
def register_controllers(api):
    api.add_namespace(paciente_ns)