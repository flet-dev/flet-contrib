import flet as ft

from flet_contrib.color_picker import HueSlider


def main(page: ft.Page):
    def hue_changed(hue):
        print(hue)

    hue_slider = HueSlider(on_change_hue=hue_changed)

    page.add(hue_slider)


ft.app(target=main)
