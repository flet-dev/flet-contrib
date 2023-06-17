import flet as ft

from flet_contrib.vertical_slider import VerticalSlider, HorizontalSlider


def main(page: ft.Page):
    def slider_changed(e):
        print(e.control.value)

    # horizonal_slider1 = HorizontalSlider()
    horizonal_slider12 = VerticalSlider(min=0, max=500, value=500, divisions=5)
    vertical_slider = VerticalSlider(
        vertical=True,
        divisions=10,
        min=100,
        max=600,
        value=500,
    )
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
        ft.Row(
            [horizonal_slider12],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        # default_slider,
        vertical_slider,
    )


ft.app(target=main)
