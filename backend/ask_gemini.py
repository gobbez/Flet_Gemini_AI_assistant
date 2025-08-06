from typing import Dict

import google.generativeai as genai
from keys import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


async def ask_gemini(prompt: str) -> Dict:
    """
    Call Google Gemini API Key
    :param prompt: user prompt
    :return: the answer and the settings params
    """
    try:
        response = model.generate_content(prompt).text.strip()

    except Exception as e:
        response = f"Gemini Error: {str(e)}"

    answer = {
        "response": response,
    }
    return answer
