from openai import OpenAI
import time
import json
import os
from src.service.chat_service import ChatService

class ThreadService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.assistant_id = os.environ.get("ASSISTANT_ID")
        self.chat_service = ChatService()
    
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
        tool_outputs = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            print("Processing function:", function_name)
            arguments = json.loads(tool_call.function.arguments)
            output = self.chat_service.execute_function(function_name, arguments)
            
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(output)
            })
            
        if tool_outputs:
            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
            
    def get_latest_message(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id)
        return messages.data[0].content[0].text.value