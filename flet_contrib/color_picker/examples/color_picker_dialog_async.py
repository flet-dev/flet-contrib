import flet as ft

from flet_contrib.color_picker import ColorPicker


async def main(page: ft.Page):
    async def open_color_picker(e):
        d.open = True
        await page.update_async()

    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker)

    async def change_color(e):
        color_icon.icon_color = color_picker.color
        d.open = False
        await page.update_async()

    async def close_dialog(e):
        d.open = False
        await d.update_async()

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

    await page.add_async(color_icon)


ft.app(main)
