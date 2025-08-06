# -*- coding: utf-8 -*-

import flet as ft
from backend.main_backend import AIBackend
from frontend.components.component_switch_theme import component_switch_theme
from frontend.settings.page_settings import main_settings
from marketplace.ai_marketplace import available_ai
import asyncio

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


def main(page: ft.Page):
    """
    Main frontend function to create the frontend part
    :param page: chat page
    """
    # Load settings
    page, chat_users, current_chat = main_settings(page)
    chat_available = True

    # Store messages separately for each chat
    chat_history = {user: ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO) for user in chat_users}

    messages = chat_history[current_chat]

    input_field = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
    )

    def add_message(text: str, sender: str, target_chat: str = None):
        """
        Add the message on the current chat
        :param text: message received (from user or AI)
        :param sender: the sender (user or AI)
        :param target_chat: the chat to send the message
        """
        color = "#E0E0E0" if sender == "user" else aval_ai[target_chat]['color']
        align = ft.MainAxisAlignment.END if sender == "user" else ft.MainAxisAlignment.START
        bubble = ft.Container(
            content=ft.Text(
                f"{text}",
                selectable=True,
                font_family="Arial",
            ),
            bgcolor=color,
            padding=10,
            border_radius=20,
            width=800,
        )
        chat_history[target_chat].controls.append(
            ft.Row([bubble], alignment=align)
        )
        page.update()

    def on_submit(e):
        """
        Call backend in order to receive AI answer and update page
        :param e: required but not used
        """
        nonlocal current_chat, chat_available
        user_text = input_field.value.strip()
        if not user_text or not chat_available:
            return

        chat_available = False
        original_chat = current_chat
        add_message(user_text, "user", target_chat=original_chat)
        input_field.value = ""
        page.update()

        backend = asyncio.run(get_ai_reply(user_text, original_chat))
        add_message(backend.response, "bot", target_chat=original_chat)

        while backend.is_recursive:
            chat_available = False
            backend = asyncio.run(get_ai_reply(user_text, original_chat))
            add_message(backend.response, "bot", target_chat=original_chat)

        chat_available = True

    send_button = ft.IconButton(icon=ft.Icons.SEND, on_click=on_submit)

    chat_input = ft.Row(
        controls=[input_field, send_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def on_chat_select(e):
        """
        Change chat when user clicks on a name
        :param e: chat control
        """
        nonlocal messages, current_chat
        selected = e.control.data
        if selected == current_chat:
            return
        current_chat = selected
        messages_column.controls[0] = chat_history[current_chat]
        page.update()

    # Sidebar with chat names
    chat_list = ft.Column()
    for user in chat_users:
        chat_list.controls.append(
            ft.TextButton(text=user, data=user, on_click=on_chat_select)
        )

    # Container for dynamic messages
    messages_column = ft.Column(
        controls=[messages],
        expand=True,
    )

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=component_switch_theme(page),
                            alignment=ft.alignment.top_right,
                            padding=ft.padding.only(bottom=10),
                        ),
                        ft.Container(
                            content=chat_list,
                            width=200,
                            bgcolor="#F0F0F0",
                            padding=10,
                        ),
                    ],
                ),
                ft.Column(
                    controls=[
                        ft.Text("Skybound AI", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        messages_column,
                        chat_input
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
            expand=True
        )
    )

    page.update()


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)