from typing import Dict

from backend.ask_gemini import ask_gemini
import datetime


async def file_method(msg: str) -> Dict:
    """
    Create a file on the user local folder
    :param msg: the prompt of the user (with requirements and the file format)
    :return: the answer and the settings params
    """
    query = msg[2:].strip()
    output = await ask_gemini(query)
    response = output['response']

    suffix = ".txt"
    if "python" in query.lower():
        suffix = ".py"
    # @todo add other file types

    with open(f"file_{datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S')}{suffix}", 'w') as f:
        f.write(response)
        answer = {
            "response": f"Created file!\nPath: {f.name}"
        }
        return answer
