from src.controller.paciente_controller import paciente_ns
from src.controller.chat_controller import chat_ns

#Registro de namespeaces
def register_controllers(api):
    api.add_namespace(paciente_ns)
    api.add_namespace(chat_ns)