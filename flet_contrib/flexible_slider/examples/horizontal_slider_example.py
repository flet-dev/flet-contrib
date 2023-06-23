import flet as ft

from flet_contrib.flexible_slider import FlexibleSlider


def main(page: ft.Page):
    def horizontal_slider_changed():
        print(horizontal_slider.value)

    horizontal_slider = FlexibleSlider(
        # divisions=10,
        min=100,
        max=600,
        value=500,
        thickness=10,
        active_color=ft.colors.BLUE_500,
        inactive_color=ft.colors.YELLOW_300,
        thumb_color=ft.colors.GREEN,
        thumb_radius=15,
        on_change=horizontal_slider_changed,
    )

    page.add(
        horizontal_slider,
    )


ft.app(target=main)
