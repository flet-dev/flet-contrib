import flet as ft

from flet_contrib.color_picker import HueSlider


def main(page: ft.Page):
    def hue_changed():
        print(hue_slider.hue)

    hue_slider = HueSlider(on_change_hue=hue_changed)

    page.add(hue_slider)

    new_hue = ft.TextField(label="Value between 0 and 1, e.g. 0.5")

    def update_hue(e):
        hue_slider.hue = float(new_hue.value)
        # hue_slider.update_hue_slider(new_hue.value)
        hue_slider.update()

    page.add(new_hue, ft.FilledButton("Update hue", on_click=update_hue))


ft.app(target=main)
