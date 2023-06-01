import flet as ft
import colorsys
from .utils import *

SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1):
        super().__init__()
        self.__hue = hue
        self.__number_of_hues = 10
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_slider()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag

    # hue
    @property
    def hue(self) -> float:
        return self.__hue

    @hue.setter
    def hue(self, value: float):
        if isinstance(value, float):
            self.__hue = value
            if value < 0 or value > 1:
                raise Exception("Hue value should be between 0 and 1")
        else:
            raise Exception("Hue value should be a float number")

    def _before_build_command(self):
        super()._before_build_command()
        # called every time on self.update()
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))

    def update_selected_hue(self, x):
        self.__hue = max(0, min((x - CIRCLE_SIZE / 2) / self.track.width, 1))
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))
        self.thumb.update()
        self.on_change_hue()

    def start_drag(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_x)

    def drag(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_x)

    def generate_gradient_colors(self):
        colors = []
        for i in range(0, self.__number_of_hues + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / self.__number_of_hues, 1, 1))
            colors.append(color)
        return colors

    def generate_slider(self):
        self.track = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.generate_gradient_colors(),
            ),
            width=SLIDER_WIDTH - CIRCLE_SIZE,
            height=CIRCLE_SIZE / 2,
            border_radius=5,
            top=CIRCLE_SIZE / 4,
            left=CIRCLE_SIZE / 2,
        )

        self.thumb = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.content.controls.append(self.track)
        self.content.controls.append(self.thumb)
