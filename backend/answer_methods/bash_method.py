import subprocess
from typing import Dict


def bash_method(msg: str) -> Dict:
    """
    Execute a bash command
    :param msg: the user command
    :return: the answer and the settings params
    """
    command = msg[1:].strip()

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        output = result.stdout.strip()

    except subprocess.CalledProcessError as e:
        output = f"Error:\n{e.stderr.strip()}"

    answer = {
        "response": f"Executed:\n{command}\n\n{output}",
    }
    return answer
