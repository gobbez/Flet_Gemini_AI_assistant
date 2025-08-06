import flet as ft


def component_switch_theme(page):
    """
    Component-like function to create a light-dark theme switch
    :param page: the page of the chat
    :return: the switch component
    """
    def change_theme_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch_theme.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            switch_theme.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    switch_theme = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=change_theme_mode)

    return switch_theme
