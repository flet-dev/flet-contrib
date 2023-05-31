import flet as ft
import colorsys
from .utils import *

SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1, number_of_hues=5):
        super().__init__()
        self.__hue = hue
        self.__number_of_hues = number_of_hues
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_hues()
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

    # number of hues
    @property
    def number_of_hues(self) -> int:
        return self.__number_of_hues

    @number_of_hues.setter
    def number_of_hues(self, value: int):
        self.__number_of_hues = value

    def _before_build_command(self):
        super()._before_build_command()
        # called every time on self.update()
        self.circle.left = self.__hue * (SLIDER_WIDTH - CIRCLE_SIZE)
        self.circle.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))

    def update_selected_hue(self, x):
        self.__hue = max(
            0, min((x - CIRCLE_SIZE / 2) / (SLIDER_WIDTH - CIRCLE_SIZE), 1)
        )
        self.circle.left = self.__hue * (SLIDER_WIDTH - CIRCLE_SIZE)
        self.circle.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))
        self.circle.update()
        self.on_change_hue(self.__hue)

    def start_drag(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_x)

    def drag(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_x)

    def generate_hues(self):
        # self.hue_width = (self.content.width - CIRCLE_SIZE) / (self.number_of_hues + 1)
        self.hue_width = (SLIDER_WIDTH - CIRCLE_SIZE) / (self.__number_of_hues + 1)
        for i in range(0, self.__number_of_hues + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / self.__number_of_hues, 1, 1))
            if i == 0:
                border_radius = ft.border_radius.only(top_left=5, bottom_left=5)
            elif i == self.__number_of_hues:
                border_radius = ft.border_radius.only(top_right=5, bottom_right=5)
            else:
                border_radius = None
            self.content.controls.append(
                ft.Container(
                    height=CIRCLE_SIZE / 2,
                    width=self.hue_width,
                    bgcolor=color,
                    border_radius=border_radius,
                    top=CIRCLE_SIZE / 4,
                    left=i * self.hue_width + CIRCLE_SIZE / 2,
                )
            )

        self.circle = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.content.controls.append(self.circle)
