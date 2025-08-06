import datetime
from typing import Dict

from backend.ask_gemini import ask_gemini
from backend.answer_methods.bash_method import bash_method
from backend.answer_methods.file_method import file_method
from backend.answer_methods.recursive_bash import recursive_bash
from backend.answer_methods.recursive_chat import recursive_chat


class AIBackend:
    def __init__(self):
        self.user_text = ''
        self.current_chat = ''
        self.response = ''
        self.history = []
        self.h_time = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        self.is_recursive = True
        self.task = {}
        self.memory = {}
        self.number = {}

    def save_history(self, context):
        """
        Save the conversation history in a txt file
        :param context: The member (User or Bot) and the message written
        """
        self.history.append(context)
        with open(f"history_{self.h_time}.txt", "a") as h_file:
            h_file.write(f"\n{context}")

    async def get_response(self, msg: str, current_chat: str) -> Dict:
        """
        Main backend function to let AI answer based on the user command, task and chat
        :param msg: the prompt or command sent by the user
        :param current_chat: the current chat
        :return: the answer and the settings params
        """
        self.save_history(f"User: {msg}")
        msg = msg.strip()

        # File generation
        if msg.startswith("-f"):
            answer = await file_method(msg)
            return answer

        # Bash command
        elif msg.startswith(":"):
            answer = bash_method(msg)
            return answer

        # Recursive chat loop
        elif msg.startswith("-r"):
            answer = await recursive_chat(self, current_chat)
            return answer

        # Recursive bash loop
        elif msg.startswith("-:r"):
            answer = await recursive_bash(self, current_chat)
            return answer

        # Default mode
        else:
            prompt = "\n".join(self.history + [f"User: {msg}"])
            answer = await ask_gemini(prompt)
            return answer


