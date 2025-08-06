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
        with open(f"history_{self.h_time}.txt", "a", encoding="utf-8") as h_file:
            h_file.write(f"\n{context}")

    async def get_response(self, prompt: str, user_text: str, current_chat: str) -> Dict:
        """
        Main backend function to let AI answer based on the user command, task and chat
        :param prompt: the AI settings + the prompt or command sent by the user
        :param user_text: the message or command written by the user
        :param current_chat: the current chat
        :return: the answer and the settings params
        """
        self.save_history(f"\n\nUser: {user_text}\n")
        prompt = prompt.strip()

        # File generation
        if user_text.startswith("-f"):
            answer = await file_method(prompt)
            return answer

        # Bash command
        elif user_text.startswith(":"):
            answer = bash_method(user_text)
            return answer

        # Recursive chat loop
        elif user_text.startswith("-r"):
            answer = await recursive_chat(self, current_chat)
            return answer

        # Recursive bash loop
        elif user_text.startswith("-:r"):
            answer = await recursive_bash(self, current_chat)
            return answer

        # Default mode
        else:
            prompt = "\n".join(self.history + [f"User: {prompt}"])
            answer = await ask_gemini(prompt)
            return answer


