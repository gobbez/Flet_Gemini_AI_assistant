import asyncio
from backend.ask_gemini import ask_gemini
from backend.answer_methods.bash_method import bash_method


async def recursive_bash(user_data):
    memory = user_data.memory
    task = user_data.user_text[3:].strip()
    number = user_data.number

    context_text = (
        f"User request: {task}\n"
        "You are a Linux bash assistant and a Penetration Tester. "
        "You have full access to every tool via shell. Generate only one shell command at a time. "
        "Never write comments, introductions or explanations. Write the shell command only. "
        "Do not include backticks or any Markdown characters in your output. Only give plain bash command."
    )

    full_output = ""

    number += 1
    full_context = f"{context_text}\nPrevious context:\n" + "\n".join(memory)
    gemini_response = await ask_gemini(full_context)
    command = gemini_response['response'].strip().replace("`", "")

    # Call bash_method starting the command with :
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
        answer = {
            "is_recursive": False,
            "response": full_output,
            "task": "",
            "memory": [],
            "number": 0,
        }
    else:
        full_output += f"Continuing...\n"
        answer = {
            "is_recursive": True,
            "response": full_output,
            "task": task,
            "memory": memory,
            "number": number,
        }

    await asyncio.sleep(3)
    return answer
