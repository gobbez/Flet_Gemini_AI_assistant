import asyncio
from typing import Dict

from backend.ask_gemini import ask_gemini


async def recursive_chat(user_data, current_chat) -> Dict:
    """
   The AI will chat with itself recursively.
   It will write one message, pass it as its next input and continue until the user task is completed.
   :param user_data: user data and settings, received from main_backend
   :param current_chat: the current chat
   :return: the answer and the settings params, one for each iteration
   """
    if current_chat not in user_data.memory:
        user_data.memory[current_chat] = []
    if current_chat not in user_data.task:
        user_data.task[current_chat] = ""
    if current_chat not in user_data.number:
        user_data.number[current_chat] = 0

    task = user_data.user_text[3:].strip()
    user_data.task[current_chat] = task
    number = user_data.number[current_chat]
    memory = user_data.memory[current_chat]

    context_text = (
        f"User request: {task}\n"
        "You must write one message or explanation at a time. "
        "You are in an infinite loop where you will receive the output of the previous message you wrote. "
        "The process where you are in is: user input -> your output -> your output -> your output.. until solution. "
    )

    full_output = ""

    number += 1
    full_context = f"{context_text}\nPrevious context:\n" + "\n".join(memory)
    gemini_response = await ask_gemini(full_context)
    response = gemini_response['response']

    full_output += f"Answer {number}: {response}\n\n"
    memory.append(f"Answer {number}: {response}")

    done_prompt = (
        f"Task: {task}\nContext:\n{chr(10).join(memory)}\n\n"
        "Is the task complete? If yes, start your answer with DONE and the solution "
        "(example message:'DONE the solution is...'), if not solved write only 'no'."
    )

    await asyncio.sleep(1)
    done_check_gemini = await ask_gemini(done_prompt)
    done_check = done_check_gemini['response']

    if "DONE" in done_check.upper():
        full_output += f"DONE\n{done_check}"
        is_recursive = False

        # Reset for this chat
        user_data.memory[current_chat] = []
        user_data.task[current_chat] = ""
        user_data.number[current_chat] = 0

    else:
        full_output += f"Continuing...\n"
        is_recursive = True

    answer = {
        "is_recursive": is_recursive,
        "response": full_output,
        "task": user_data.task,
        "memory": user_data.memory,
        "number": user_data.number,
    }

    await asyncio.sleep(3)
    return answer
