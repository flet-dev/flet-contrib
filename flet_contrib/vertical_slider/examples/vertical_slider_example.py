import flet as ft

from flet_contrib.vertical_slider import VerticalSlider


def main(page: ft.Page):
    vertical_slider = VerticalSlider()

    page.add(vertical_slider)


ft.app(target=main)
