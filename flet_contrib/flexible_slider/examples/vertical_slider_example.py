import flet as ft

from flet_contrib.flexible_slider import FlexibleSlider


async def main(page: ft.Page):
    def vertical_slider_changed():
        print(vertical_slider.value)

    vertical_slider = FlexibleSlider(
        vertical=True,
        divisions=5,
        on_change=vertical_slider_changed,
    )

    page.add(
        vertical_slider,
    )


ft.app(target=main)
