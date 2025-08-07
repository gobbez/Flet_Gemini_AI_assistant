import flet as ft
from marketplace.ai_marketplace import available_ai

aval_ai = available_ai()


def component_add_message(page, chat_history, user_color, text: str, sender: str, target_chat: str):
    """
    Add the message bubble to the UI in the specified chat.
    """
    if sender == "user":
        color = user_color[0] if page.theme_mode == ft.ThemeMode.LIGHT else user_color[1]
    else:
        color_key = "color_light" if page.theme_mode == ft.ThemeMode.LIGHT else "color_dark"
        color = aval_ai[target_chat].get(color_key, "#B0BEC5")

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
