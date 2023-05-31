import flet as ft

from flet_contrib.color_picker import ColorPicker


def main(page: ft.Page):
    color_picker = ColorPicker(color="#c8df6f")

    d = ft.AlertDialog(content=color_picker)
    page.dialog = d

    def open_color_picker(e):
        d.open = True
        page.update()

    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))


ft.app(target=main)
