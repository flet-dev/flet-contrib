import flet as ft

from flet_contrib.vertical_slider import FlexibleSlider


def main(page: ft.Page):
    def horizontal_slider_changed():
        print(horizontal_slider.value)

    horizontal_slider = FlexibleSlider(
        # divisions=10,
        min=100,
        max=600,
        value=500,
        selected_track_color=ft.colors.BLUE_500,
        track_color=ft.colors.YELLOW_300,
        thumb_color=ft.colors.GREEN,
        thumb_radius=5,
        on_change=horizontal_slider_changed,
    )

    page.add(
        horizontal_slider,
    )


ft.app(target=main)
