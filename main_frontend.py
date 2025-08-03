# -*- coding: utf-8 -*-

import flet as ft
from backend.main_backend import AIBackend
import asyncio

ai_backend = AIBackend()


async def get_ai_reply(user_text):
    ai_backend.user_text = user_text
    answer = await ai_backend.get_response(ai_backend.user_text)

    ai_backend.is_recursive = answer.get('is_recursive', False)
    ai_backend.task = answer.get('task', '')
    ai_backend.memory = answer.get('memory', [])
    ai_backend.response = answer.get('response', '')
    ai_backend.number = answer.get('number', 0)

    ai_backend.save_history(f"Bot: {ai_backend.response}")
    return


def main(page: ft.Page):
    page.title = "AI Chat"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 400
    page.window_height = 700
    page.padding = 10

    messages = ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    input_field = ft.TextField(
        hint_text="Scrivi un messaggio...",
        autofocus=True,
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
    )

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
        messages.controls.append(
            ft.Row([bubble], alignment=align)
        )
        page.update()

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

    page.add(
        ft.Column(
            controls=[
                ft.Text("Your AI Assistant", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                messages,
                chat_input
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )

    page.update()

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)


