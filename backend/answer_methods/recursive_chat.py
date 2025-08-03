import asyncio
from backend.ask_gemini import ask_gemini


async def recursive_chat(user_data):
    memory = user_data.memory
    task = user_data.user_text[3:].strip()
    number = user_data.number

    context_text = f"User request: {task}"

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
