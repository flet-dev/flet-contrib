import flet as ft

from flet_contrib.color_picker import ColorPicker


def main(page: ft.Page):
    def open_color_picker(e):
        d.open = True
        page.update()

    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker)

    def change_color(e):
        color_icon.icon_color = color_picker.color
        d.open = False
        page.update()

    def close_dialog(e):
        d.open = False
        d.update()

    d = ft.AlertDialog(
        content=color_picker,
        actions=[
            ft.TextButton("OK", on_click=change_color),
            ft.TextButton("Cancel", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=change_color,
    )
    page.dialog = d

    page.add(color_icon)


ft.app(target=main)
