# -*- coding: utf-8 -*-

import flet as ft
from backend.main_backend import AIBackend
import asyncio

ai_backend = AIBackend()


async def get_ai_reply(user_text):
    """
    Async call to AI
    :param user_text: user message/prompt/command
    :return: updates ai_backend dictionary
    """
    ai_backend.user_text = user_text
    answer = await ai_backend.get_response(ai_backend.user_text)

    ai_backend.response = answer.get('response', '')
    ai_backend.is_recursive = answer.get('is_recursive', False)
    ai_backend.task = answer.get('task', {})
    ai_backend.memory = answer.get('memory', {})
    ai_backend.number = answer.get('number', {})

    ai_backend.save_history(f"Bot: {ai_backend.response}")
    return


def main(page: ft.Page):
    page.title = "AI Chat"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 500
    page.window_height = 700
    page.padding = 10

    # List of available chats
    chat_users = ["Alice", "Bob", "Gruppo"]
    ai_backend.current_chat = "Alice"

    # Store messages separately for each chat
    chat_history = {user: ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO) for user in chat_users}

    messages = chat_history[ai_backend.current_chat]

    input_field = ft.TextField(
        hint_text="Scrivi un messaggio...",
        autofocus=True,
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
    )

    # Add message to the correct chat
    def add_message(text: str, sender: str):
        color = "#E0E0E0" if sender == "user" else "#DCF8C6"
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
            width=300,
        )
        chat_history[ai_backend.current_chat].controls.append(
            ft.Row([bubble], alignment=align)
        )
        page.update()

    # Handle message send
    def on_submit(e):
        user_text = input_field.value.strip()
        if not user_text:
            return
        add_message(user_text, "user")
        input_field.value = ""
        page.update()

        asyncio.run(get_ai_reply(user_text))
        add_message(ai_backend.response, "bot")

        while ai_backend.is_recursive:
            asyncio.run(get_ai_reply(user_text))
            add_message(ai_backend.response, "bot")

    send_button = ft.IconButton(icon=ft.Icons.SEND, on_click=on_submit)

    chat_input = ft.Row(
        controls=[input_field, send_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Change chat when user clicks on a name
    def on_chat_select(e):
        nonlocal messages
        selected = e.control.data
        if selected == ai_backend.current_chat:
            return
        ai_backend.current_chat = selected
        messages_column.controls[0] = chat_history[ai_backend.current_chat]
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
                ft.Container(
                    content=chat_list,
                    width=100,
                    bgcolor="#F0F0F0",
                    padding=10,
                ),
                ft.Column(
                    controls=[
                        ft.Text("Your AI Assistant", size=24, weight=ft.FontWeight.BOLD),
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