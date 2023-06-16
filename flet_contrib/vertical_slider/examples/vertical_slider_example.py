import flet as ft

from flet_contrib.vertical_slider import VerticalSlider, HorizontalSlider


def main(page: ft.Page):
    def slider_changed(e):
        print(e.control.value)

    horizonal_slider = HorizontalSlider()
    vertical_slider = VerticalSlider()
    default_slider = ft.Slider(
        min=0,
        max=100,
        value=50,
        width=200,
        divisions=10,
        label="{value}",
        on_change=slider_changed,
    )

    page.add(
        ft.Row([horizonal_slider], alignment=ft.MainAxisAlignment.CENTER),
        default_slider,
        vertical_slider,
    )


ft.app(target=main)
