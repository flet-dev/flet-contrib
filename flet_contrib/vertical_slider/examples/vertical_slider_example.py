import flet as ft

from flet_contrib.vertical_slider import VerticalSlider, HorizontalSlider


def main(page: ft.Page):
    horizonal_slider = HorizontalSlider()
    vertical_slider = VerticalSlider()

    page.add(vertical_slider, horizonal_slider)


ft.app(target=main)
