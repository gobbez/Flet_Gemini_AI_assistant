import asyncio
from backend.ask_gemini import ask_gemini
from backend.answer_methods.bash_method import bash_method


async def recursive_bash(user_data, current_chat):
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
        "You are a Linux bash assistant and a Penetration Tester. "
        "You have full access to every tool via shell. Generate only one shell command at a time. "
        "Never write comments, introductions or explanations. Write the shell command only. "
        "Do not include backticks or any Markdown characters in your output. Only give plain bash command."
    )

    full_output = ""

    number += 1
    user_data.number[current_chat] = number

    full_context = f"{context_text}\nPrevious context:\n" + "\n".join(memory)
    gemini_response = await ask_gemini(full_context)
    command = gemini_response['response'].strip().replace("`", "")

    bash_output = bash_method(":" + command)
    output = bash_output['response']

    full_output += f"Command {number}: {command}\nOutput:\n{output}\n\n"
    memory.append(f"Command {number}: {command}\nOutput:\n{output}")

    done_prompt = (
        f"Task: {task}\nContext:\n{chr(10).join(memory)}\n\n"
        "Is the task complete? If yes, start your answer with DONE and the solution "
        "(example message:'DONE the solution is...'), if not solved write only 'no'."
    )

    done_check_gemini = await ask_gemini(done_prompt)
    done_check = done_check_gemini['response']

    if "DONE" in done_check.upper():
        full_output += f"DONE \n{done_check}"
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
