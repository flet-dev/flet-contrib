import flet as ft
import colorsys
from .utils import *

SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1, number_of_hues=10):
        super().__init__()
        self.hue = hue
        self.number_of_hues = number_of_hues
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_hues()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag

    def update_hue_slider(self, hue):
        self.hue = hue
        x = self.hue * self.number_of_hues * self.hue_width + CIRCLE_SIZE
        self.update_selected_hue(x)

    def find_hue(self, x):
        for hue_block in self.content.controls[
            :-1
        ]:  # excluding the last element of the stack controls list which is the circle
            if x >= hue_block.left and x <= hue_block.left + self.hue_width:
                color = hue_block.bgcolor
                rgb_color = hex2rgb(color)
                hsv_color = colorsys.rgb_to_hsv(
                    round(rgb_color[0] / 255, 1),
                    round(rgb_color[1] / 255, 1),
                    round(rgb_color[2] / 255, 1),
                )
                self.hue = hsv_color[0]

    def update_selected_hue(self, x):
        self.find_hue(x)
        color = rgb2hex(colorsys.hsv_to_rgb(self.hue, 1, 1))
        self.circle.left = max(
            0,
            min(
                x - CIRCLE_SIZE / 2,
                self.hue_width * ((self.number_of_hues + 1)),
            ),
        )

        self.circle.bgcolor = color
        self.circle.update()
        self.on_change_hue(self.hue)

    def start_drag(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_x)

    def drag(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_x)

    def generate_hues(self):
        self.hue_width = (self.content.width - CIRCLE_SIZE) / (self.number_of_hues + 1)
        for i in range(0, self.number_of_hues + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / self.number_of_hues, 1, 1))
            if i == 0:
                border_radius = ft.border_radius.only(top_left=5, bottom_left=5)
            elif i == self.number_of_hues:
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
