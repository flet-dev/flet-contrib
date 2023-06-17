import flet as ft

from flet_contrib.vertical_slider import FlexibleSlider


def main(page: ft.Page):
    def vertical_slider_changed():
        print(vertical_slider.value)

    vertical_slider = FlexibleSlider(
        vertical=True,
        divisions=10,
        min=100,
        max=600,
        value=500,
        on_change=vertical_slider_changed,
    )

    page.add(
        vertical_slider,
    )


ft.app(target=main)
