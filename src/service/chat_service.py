# src/service/chat_service.py
from openai import OpenAI
import json
import time
import os
from src.model.db import db
from src.service.paciente_service import PacienteService
from src.schemas.paciente_schema import PacienteSchema

class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.assistant_id = os.environ.get("ASSISTANT_ID")
        self.paciente_service = PacienteService()
        self.paciente_schema = PacienteSchema()

    def create_thread(self):
        return self.client.beta.threads.create()

    def add_message(self, thread_id, message):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

    def process_message(self, thread_id, user_input):
        self.add_message(thread_id, user_input)
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        return self.handle_run(thread_id, run.id)

    def handle_run(self, thread_id, run_id):
        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "requires_action":
                self.handle_required_actions(run, thread_id, run_id)
            elif run.status in ["completed", "failed", "cancelled"]:
                break
            time.sleep(1)
        return self.get_latest_message(thread_id)

    def handle_required_actions(self, run, thread_id, run_id):
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            output = self.execute_function(function_name, arguments)
            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=[{
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(output)
                }]
            )

    def execute_function(self, function_name, arguments):
        if function_name == "fetch_patient_info":
            return self.fetch_patient_info(arguments)
        elif function_name == "create_patient":
            return self.create_patient(arguments)
        elif function_name == "get_appointment_availability":
            return self.get_appointment_availability(arguments)
        elif function_name == "confirm_appointment":
            return self.confirm_appointment(arguments)
        elif function_name == "book_appointment":
            return self.book_appointment(arguments)
        return "Function not handled"

    def fetch_patient_info(self, arguments):
        dni = arguments['patient_dni']
        paciente = self.paciente_service.obtener_paciente_por_dni(dni)
        if paciente:
            paciente_info = self.paciente_schema.dump(paciente)
            return paciente_info
        else:
            return "Paciente no encontrado"

    def create_patient(self, arguments):
        paciente = self.paciente_schema.load(arguments)
        nuevo_paciente = self.paciente_service.agregar_paciente(paciente)
        return self.paciente_schema.dump(nuevo_paciente)

    def get_latest_message(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id)
        return messages.data[0].content[0].text.value

