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
            "color_light": "#FCBA03",
            "color_dark": "#4D3800",
        },
        "Code_Expert": {
            "role": "Code assistant",
            "style": "Funny but technical",
            "color_light": "#ABDAFF",
            "color_dark": "#36454F",
        }
    }
    return ai_dict
