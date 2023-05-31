import flet as ft

from flet_contrib.color_picker import ColorPicker


def main(page: ft.Page):
    color_picker = ColorPicker(color="#c8df6f")
    new_color = ft.TextField(width=100)

    def change_color(e):
        color_picker.color = new_color.value
        color_picker.update()

    page.add(
        color_picker, new_color, ft.FilledButton("Change color", on_click=change_color)
    )


ft.app(target=main)
