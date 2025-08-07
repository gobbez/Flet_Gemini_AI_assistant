# backend/functions/ai_requests.py

from backend.main_backend import AIBackend
from marketplace.ai_marketplace import available_ai

aval_ai = available_ai()
chat_backends = {user: AIBackend() for user in aval_ai.keys()}


async def get_ai_reply(user_text, current_chat):
    """
    Async call to AI
    :param user_text: user message/prompt/command
    :param current_chat: the current chat opened by the user
    :return: updates ai_backend dictionary
    """
    ai_role_style_prompt = f"These are your details: {aval_ai[current_chat]}. You must behave accordingly."
    ai_backend = chat_backends[current_chat]
    ai_backend.user_text = user_text
    prompt = f"{ai_role_style_prompt}. This is the user prompt: {user_text}"
    answer = await ai_backend.get_response(prompt, user_text, current_chat)

    ai_backend.response = answer.get('response', '')
    ai_backend.is_recursive = answer.get('is_recursive', False)
    ai_backend.task = answer.get('task', {})
    ai_backend.memory = answer.get('memory', {})
    ai_backend.number = answer.get('number', {})

    ai_backend.save_history(f"{current_chat}: {ai_backend.response}")
    return ai_backend
