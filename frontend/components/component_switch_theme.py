import flet as ft
from marketplace.ai_marketplace import available_ai

aval_ai = available_ai()


def component_switch_theme(page, chat_history, user_color, sidebar_colors, sidebar_container):
    """
    Component-like function to create a light-dark theme switch
    :param page: the page of the chat
    :param chat_history: the dict with all chat messages
    :param user_color: list for main page theme colors
    :param sidebar_colors: list for sidebar theme colors
    :param sidebar_container: the sidebar container to update color when theme changes
    :return: the switch component
    """
    def update_all_bubble_colors():
        for chat_name, chat_column in chat_history.items():
            for row in chat_column.controls:
                if isinstance(row, ft.Row) and row.controls:
                    container = row.controls[0]
                    if isinstance(container, ft.Container):
                        is_user = row.alignment == ft.MainAxisAlignment.END

                        if is_user:
                            color = user_color[0] if page.theme_mode == ft.ThemeMode.LIGHT else user_color[1]
                        else:
                            color_key = "color_light" if page.theme_mode == ft.ThemeMode.LIGHT else "color_dark"
                            color = aval_ai[chat_name].get(color_key, "#B0BEC5")

                        container.bgcolor = color

    def change_theme_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch_theme.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            switch_theme.thumb_icon = ft.Icons.DARK_MODE

        update_all_bubble_colors()

        # Update sidebar theme color
        sidebar_container.bgcolor = sidebar_colors[0] if page.theme_mode == ft.ThemeMode.LIGHT else sidebar_colors[1]

        page.update()

    switch_theme = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=change_theme_mode)
    return switch_theme
