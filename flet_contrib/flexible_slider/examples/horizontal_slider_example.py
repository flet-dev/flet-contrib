import flet as ft

from flet_contrib.flexible_slider import FlexibleSlider


def main(page: ft.Page):
    def horizontal_slider_changed():
        print(horizontal_slider.value)

    horizontal_slider = FlexibleSlider(
        min=100,
        max=600,
        value=250,
        thickness=10,
        length=200,
        active_color=ft.Colors.BLUE_500,
        inactive_color=ft.Colors.YELLOW_300,
        thumb_color=ft.Colors.GREEN,
        thumb_radius=20,
        on_change=horizontal_slider_changed,
    )
    # horizontal_slider.content.bgcolor = ft.Colors.AMBER
    page.add(
        horizontal_slider,
    )


ft.app(target=main)
