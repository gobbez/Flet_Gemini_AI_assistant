# -*- coding: utf-8 -*-

import flet as ft
from backend.ai_requests import get_ai_reply
from backend.main_backend import AIBackend
from frontend.components.component_switch_theme import component_switch_theme
from frontend.components.component_add_message import component_add_message
from frontend.settings.page_settings import main_settings
from marketplace.ai_marketplace import available_ai
import asyncio

aval_ai = available_ai()
chat_backends = {user: AIBackend() for user in aval_ai.keys()}


def main(page: ft.Page):
    """
    Main frontend function to create the frontend part
    :param page: chat page
    """
    # Load settings
    page, chat_users, current_chat, user_color, sidebar_colors = main_settings(page)
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
        component_add_message(page, chat_history, user_color, user_text, "user", target_chat=original_chat)
        input_field.value = ""
        page.update()

        backend = asyncio.run(get_ai_reply(user_text, original_chat))
        component_add_message(page, chat_history, user_color, backend.response, "bot", target_chat=original_chat)

        while backend.is_recursive:
            chat_available = False
            backend = asyncio.run(get_ai_reply(user_text, original_chat))
            component_add_message(page, chat_history, user_color, backend.response, "bot", target_chat=original_chat)

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
            ft.TextButton(
                text=user,
                data=user,
                on_click=on_chat_select
            )
        )

    # Container for dynamic messages
    messages_column = ft.Column(
        controls=[messages],
        expand=True,
    )

    # Container for sidebar chats and theme colors
    sidebar_container = ft.Container(
        content=chat_list,
        width=200,
        bgcolor=user_color[0] if page.theme_mode == ft.ThemeMode.LIGHT else user_color[1],
        padding=10,
    )

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        component_switch_theme(page, chat_history, user_color, sidebar_colors, sidebar_container),
                        sidebar_container,
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