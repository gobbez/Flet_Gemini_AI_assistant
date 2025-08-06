import flet as ft
from marketplace.ai_marketplace import available_ai

aval_ai = available_ai()


def main_settings(page):
    # Main page settings
    page.title = "AI Chat"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 500
    page.window_height = 700
    page.padding = 10

    # List of available chats
    chat_users = aval_ai.keys()
    current_chat = "Gemini"

    # User color theme: ['light', 'dark']
    user_color = ['#E0E0E0', '#424242']

    # sidebar color theme: ['light', 'dark']
    sidebar_colors = ["#F0F0F0", "#2C2C2C"]

    return page, chat_users, current_chat, user_color, sidebar_colors
