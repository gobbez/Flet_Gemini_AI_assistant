from typing import Dict


def available_ai() -> Dict:
    """
    A dict of dictionaries with every available AI in the project.
    Each AI dictionary have:
    -name of the AI (as dict key)
    -role of the AI
    -style of the AI
    -color of the AI
    :return: Dict of dictionaries, one for each AI
    """
    ai_dict = {
        "Gemini": {
            "role": "Standard AI",
            "style": "Normal",
            "color": "#FCBA03",
        },
        "Code_Expert": {
            "role": "Code assistant",
            "style": "Funny but technical",
            "color": "#8403FC",
        }
    }
    return ai_dict
